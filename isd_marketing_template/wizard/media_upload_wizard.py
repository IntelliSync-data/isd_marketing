# -*- coding: utf-8 -*-
import base64
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class MediaUploadWizard(models.TransientModel):
    _name = 'media.upload.wizard'
    _description = 'Media Upload Wizard'

    file_data = fields.Binary(string='File', required=True)
    file_name = fields.Char(string='File Name')
    storage_method = fields.Selection([
        ('local', 'Local Server'),
        ('s3', 'AWS S3')
    ], string='Storage Method', required=True, default=lambda self: self._default_storage_method())

    @api.model
    def _default_storage_method(self):
        """Get default storage method from config"""
        return self.env['ir.config_parameter'].sudo().get_param(
            'isd_marketing_template.media_storage_method', 'local'
        )

    def action_upload(self):
        """Upload file and create media library entry"""
        self.ensure_one()

        if not self.file_data:
            raise ValidationError(_('Please select a file to upload.'))

        if not self.file_name:
            raise ValidationError(_('File name is required.'))

        try:
            # Decode file data
            file_content = base64.b64decode(self.file_data)

            # Create media library entry
            media = self.env['media.library'].create_from_upload(
                self.file_name,
                file_content,
                self.storage_method
            )

            # Show success notification
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _('File uploaded successfully: %s') % media.name,
                    'type': 'success',
                    'sticky': False,
                    'next': {
                        'type': 'ir.actions.act_window_close',
                    }
                }
            }

        except Exception as e:
            _logger.exception("Failed to upload file")
            raise ValidationError(_('Failed to upload file: %s') % str(e))
