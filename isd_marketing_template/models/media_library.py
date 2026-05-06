# -*- coding: utf-8 -*-
import base64
import hashlib
import logging
import mimetypes
from io import BytesIO
from PIL import Image
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class MediaLibrary(models.Model):
    _name = 'media.library'
    _description = 'Media Library'
    _order = 'upload_date desc'

    # Basic Information
    name = fields.Char(string='File Name', required=True, index=True)
    description = fields.Text(string='Description')

    # File Data
    file_data = fields.Binary(
        string='File',
        attachment=True,
        help='File content (for local storage)'
    )
    file_size = fields.Integer(string='File Size (bytes)', readonly=True)
    file_type = fields.Selection([
        ('image', 'Image'),
        ('video', 'Video'),
        ('other', 'Other')
    ], string='File Type', compute='_compute_file_type', store=True, index=True)
    mime_type = fields.Char(string='MIME Type', readonly=True)
    extension = fields.Char(string='Extension', compute='_compute_extension', store=True)

    # Storage Information
    storage_method = fields.Selection([
        ('local', 'Local Server'),
        ('s3', 'AWS S3')
    ], string='Storage Method', required=True, readonly=True, index=True)

    # URLs
    url = fields.Char(string='Public URL', compute='_compute_url', store=True)
    s3_key = fields.Char(string='S3 Key', readonly=True, help='S3 object key for S3 storage')

    # Thumbnail
    thumbnail = fields.Binary(
        string='Thumbnail',
        attachment=True,
        compute='_compute_thumbnail',
        store=True
    )

    # Metadata
    upload_date = fields.Datetime(
        string='Upload Date',
        default=fields.Datetime.now,
        readonly=True,
        index=True
    )
    uploaded_by = fields.Many2one(
        'res.users',
        string='Uploaded By',
        default=lambda self: self.env.user,
        readonly=True
    )

    # Checksum for deduplication
    checksum = fields.Char(string='MD5 Checksum', readonly=True, index=True)

    @api.depends('name')
    def _compute_extension(self):
        """Compute file extension from filename"""
        for record in self:
            if record.name and '.' in record.name:
                record.extension = record.name.rsplit('.', 1)[1].lower()
            else:
                record.extension = ''

    @api.depends('mime_type')
    def _compute_file_type(self):
        """Determine file type based on MIME type"""
        for record in self:
            if record.mime_type:
                if record.mime_type.startswith('image/'):
                    record.file_type = 'image'
                elif record.mime_type.startswith('video/'):
                    record.file_type = 'video'
                else:
                    record.file_type = 'other'
            else:
                record.file_type = 'other'

    @api.depends('storage_method', 'file_data', 's3_key', 'name')
    def _compute_url(self):
        """Compute public URL based on storage method"""
        for record in self:
            if record.storage_method == 'local':
                # Local URL served by controller
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                record.url = f"{base_url}/media/file/{record.id}/{record.name}"
            elif record.storage_method == 's3' and record.s3_key:
                # S3 URL
                record.url = record._get_s3_url()
            else:
                record.url = ''

    @api.depends('file_data', 'file_type', 's3_key', 'storage_method')
    def _compute_thumbnail(self):
        """Generate thumbnail for images"""
        for record in self:
            if record.file_type == 'image':
                try:
                    if record.storage_method == 'local' and record.file_data:
                        # Generate thumbnail from local file
                        image_data = base64.b64decode(record.file_data)
                        image = Image.open(BytesIO(image_data))

                        # Resize to thumbnail size (200x200)
                        image.thumbnail((200, 200), Image.Resampling.LANCZOS)

                        # Convert back to base64
                        buffer = BytesIO()
                        image.save(buffer, format=image.format or 'PNG')
                        record.thumbnail = base64.b64encode(buffer.getvalue())
                    elif record.storage_method == 's3' and record.s3_key:
                        # For S3, we could download and generate thumbnail
                        # For now, use placeholder or fetch from S3
                        # TODO: Implement S3 thumbnail generation
                        record.thumbnail = False
                    else:
                        record.thumbnail = False
                except Exception as e:
                    _logger.warning(f"Failed to generate thumbnail for {record.name}: {e}")
                    record.thumbnail = False
            else:
                # Video or other file types - no thumbnail for now
                record.thumbnail = False

    def _get_s3_url(self):
        """Generate S3 URL"""
        self.ensure_one()

        if not self.s3_key:
            return ''

        # Get S3 configuration
        config = self.env['ir.config_parameter'].sudo()
        bucket = config.get_param('isd_marketing_template.media_s3_bucket')
        region = config.get_param('isd_marketing_template.media_s3_region')
        endpoint = config.get_param('isd_marketing_template.media_s3_endpoint')

        if endpoint:
            # Custom endpoint (MinIO, DigitalOcean Spaces, etc.)
            return f"{endpoint}/{bucket}/{self.s3_key}"
        else:
            # Standard AWS S3 URL
            return f"https://{bucket}.s3.{region}.amazonaws.com/{self.s3_key}"

    def action_copy_url(self):
        """Copy URL to clipboard (via JS)"""
        self.ensure_one()

        return {
            'type': 'ir.actions.client',
            'tag': 'copy_to_clipboard',
            'params': {
                'text': self.url,
            }
        }

    def action_download(self):
        """Download file"""
        self.ensure_one()

        if self.storage_method == 'local' and self.file_data:
            return {
                'type': 'ir.actions.act_url',
                'url': self.url,
                'target': 'new',
            }
        elif self.storage_method == 's3':
            return {
                'type': 'ir.actions.act_url',
                'url': self.url,
                'target': 'new',
            }

    def unlink(self):
        """Delete media and S3 file if applicable"""
        for record in self:
            if record.storage_method == 's3' and record.s3_key:
                try:
                    # Delete from S3
                    from .s3_service import S3Service
                    s3_service = S3Service.from_config(self.env)
                    s3_service.delete_file(record.s3_key)
                except Exception as e:
                    _logger.warning(f"Failed to delete S3 file {record.s3_key}: {e}")

        return super(MediaLibrary, self).unlink()

    @api.model
    def create_from_upload(self, filename, file_content, storage_method='local'):
        """Create media record from uploaded file

        Args:
            filename (str): Original filename
            file_content (bytes): File content
            storage_method (str): 'local' or 's3'

        Returns:
            media.library: Created media record
        """
        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type:
            mime_type = 'application/octet-stream'

        # Calculate checksum
        checksum = hashlib.md5(file_content).hexdigest()

        # Check for duplicate
        existing = self.search([('checksum', '=', checksum)], limit=1)
        if existing:
            _logger.info(f"File {filename} already exists with checksum {checksum}")
            return existing

        # Prepare values
        vals = {
            'name': filename,
            'mime_type': mime_type,
            'file_size': len(file_content),
            'storage_method': storage_method,
            'checksum': checksum,
        }

        if storage_method == 'local':
            # Store locally
            vals['file_data'] = base64.b64encode(file_content)
        elif storage_method == 's3':
            # Upload to S3
            try:
                from .s3_service import S3Service
                s3_service = S3Service.from_config(self.env)
                s3_key, s3_url = s3_service.upload_file(file_content, filename, mime_type)
                vals['s3_key'] = s3_key
            except Exception as e:
                _logger.exception(f"Failed to upload {filename} to S3")
                raise ValidationError(_(f"Failed to upload file to S3: {str(e)}"))

        # Create record
        media = self.create(vals)

        _logger.info(f"Created media library entry: {media.name} (ID: {media.id})")

        return media
