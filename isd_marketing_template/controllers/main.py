# -*- coding: utf-8 -*-
import base64
import logging
import json
from werkzeug.utils import secure_filename
from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)


class MarketingTemplateController(http.Controller):
    """Controller for marketing template operations"""

    @http.route('/marketing_template/render', type='json', auth='user', methods=['POST'])
    def render_template(self, template_id, data=None):
        """
        Render a template with given data

        Args:
            template_id (int): Template ID
            data (dict): Context data for rendering

        Returns:
            dict: Rendered content and subject
        """
        try:
            template = request.env['marketing.template'].browse(template_id)
            if not template.exists():
                return {
                    'success': False,
                    'error': 'Template not found'
                }

            if not data:
                data = template._get_sample_data()

            rendered_content = template.render_template(data)
            rendered_subject = template.render_subject(data) if template.template_type == 'email' else ''

            return {
                'success': True,
                'content': rendered_content,
                'subject': rendered_subject,
            }

        except Exception as e:
            _logger.exception("Error rendering template")
            return {
                'success': False,
                'error': str(e)
            }

    @http.route('/marketing_template/preview/<int:template_id>', type='http', auth='user')
    def preview_template(self, template_id, **kwargs):
        """
        Preview template in full page

        Args:
            template_id (int): Template ID

        Returns:
            Rendered HTML page
        """
        try:
            template = request.env['marketing.template'].browse(template_id)
            if not template.exists():
                return request.not_found()

            sample_data = template._get_sample_data()
            rendered_content = template.render_template(sample_data)
            rendered_subject = template.render_subject(sample_data) if template.template_type == 'email' else ''

            if template.template_type == 'email':
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Preview: {template.name}</title>
                    <style>
                        body {{
                            margin: 0;
                            padding: 20px;
                            font-family: Arial, sans-serif;
                            background: #f5f5f5;
                        }}
                        .preview-header {{
                            background: white;
                            padding: 15px;
                            border-radius: 4px;
                            margin-bottom: 20px;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                        }}
                        .preview-subject {{
                            margin: 0;
                            color: #333;
                            font-size: 18px;
                        }}
                        .preview-content {{
                            background: white;
                            padding: 20px;
                            border-radius: 4px;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                        }}
                    </style>
                </head>
                <body>
                    <div class="preview-header">
                        <h3 class="preview-subject">Subject: {rendered_subject or '(No subject)'}</h3>
                    </div>
                    <div class="preview-content">
                        {rendered_content}
                    </div>
                </body>
                </html>
                """
            else:
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Preview: {template.name}</title>
                    <style>
                        body {{
                            margin: 0;
                            padding: 20px;
                            font-family: monospace;
                            background: #f5f5f5;
                        }}
                        .preview-content {{
                            background: white;
                            padding: 20px;
                            border-radius: 4px;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                            white-space: pre-wrap;
                        }}
                    </style>
                </head>
                <body>
                    <div class="preview-content">{rendered_content}</div>
                </body>
                </html>
                """

            return request.make_response(html, headers=[('Content-Type', 'text/html')])

        except Exception as e:
            _logger.exception("Error previewing template")
            return request.make_response(
                f"<h1>Error</h1><p>{str(e)}</p>",
                headers=[('Content-Type', 'text/html')],
                status=500
            )


class TemplateAPIController(http.Controller):
    """Public API for sending emails via templates"""

    def _get_cors_headers(self):
        """Get CORS headers for cross-origin requests"""
        return [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Origin, Content-Type, Accept, Authorization, X-Requested-With'),
            ('Access-Control-Max-Age', '86400'),
            ('Access-Control-Allow-Credentials', 'true'),
        ]

    @http.route('/api/template/send', type='http', auth='public', methods=['POST', 'OPTIONS'], csrf=False)
    def send_email(self, api_key=None, template_id=None, email=None, variables=None, **kwargs):
        """
        Send email using template ID

        POST /api/template/send
        Content-Type: application/json
        {
            "template_id": 1,
            "email": "user@example.com",
            "variables": {"name": "John Doe"}
        }

        Returns:
            JSON response with CORS headers
        """
        # Handle preflight OPTIONS request
        if request.httprequest.method == 'OPTIONS':
            return request.make_response('', headers=self._get_cors_headers())

        try:
            # Parse JSON body if Content-Type is application/json
            if request.httprequest.content_type and 'application/json' in request.httprequest.content_type:
                try:
                    data = json.loads(request.httprequest.data.decode('utf-8'))
                    template_id = data.get('template_id', template_id)
                    email = data.get('email', email)
                    variables = data.get('variables', variables)
                except Exception as e:
                    return request.make_json_response({
                        'success': False,
                        'error': f'Invalid JSON: {str(e)}'
                    }, status=400, headers=self._get_cors_headers())

            # Validate required params
            if not template_id:
                return request.make_json_response({
                    'success': False,
                    'error': 'template_id is required'
                }, status=400, headers=self._get_cors_headers())

            if not email:
                return request.make_json_response({
                    'success': False,
                    'error': 'Email address is required'
                }, status=400, headers=self._get_cors_headers())

            # Find template by template_id
            template = request.env['marketing.template'].sudo().search([
                ('id', '=', template_id),
                ('active', '=', True)
            ], limit=1)

            if not template:
                return request.make_json_response({
                    'success': False,
                    'error': 'Template not found or not enabled'
                }, status=404, headers=self._get_cors_headers())

            # Send email
            result = template.send_email_via_api(email, variables or {})

            return request.make_json_response(result, headers=self._get_cors_headers())

        except Exception as e:
            _logger.exception("Error sending email via API")
            return request.make_json_response({
                'success': False,
                'error': str(e)
            }, status=500, headers=self._get_cors_headers())

    @http.route('/api/template/<string:api_key>/send', type='http', auth='public', methods=['POST', 'OPTIONS'], csrf=False)
    def send_email_http(self, api_key, **kwargs):
        """
        Send email using template API key (HTTP POST version)

        POST /api/template/<api_key>/send
        Form data:
            email: user@example.com
            variables[name]: John Doe
            variables[link]: https://...

        Returns:
            JSON response with CORS headers
        """
        # Handle preflight OPTIONS request
        if request.httprequest.method == 'OPTIONS':
            return request.make_response('', headers=self._get_cors_headers())

        try:
            # Get email from form data
            email = kwargs.get('email')
            if not email:
                return request.make_json_response({
                    'success': False,
                    'error': 'Email address is required'
                }, status=400, headers=self._get_cors_headers())

            # Parse variables from form data
            variables = {}
            for key, value in kwargs.items():
                if key.startswith('variables[') and key.endswith(']'):
                    var_name = key[10:-1]  # Extract variable name
                    variables[var_name] = value

            # Find template by API key
            template = request.env['marketing.template'].sudo().search([
                ('api_key', '=', api_key),
                ('api_enabled', '=', True),
                ('active', '=', True)
            ], limit=1)

            if not template:
                return request.make_json_response({
                    'success': False,
                    'error': 'Invalid API key or template not found'
                }, status=404, headers=self._get_cors_headers())

            # Send email
            result = template.send_email_via_api(email, variables)

            return request.make_json_response(result, headers=self._get_cors_headers())

        except Exception as e:
            _logger.exception("Error sending email via HTTP API")
            return request.make_json_response({
                'success': False,
                'error': str(e)
            }, status=500, headers=self._get_cors_headers())


class MediaLibraryController(http.Controller):
    """Controller for media library operations"""

    @http.route('/media/upload', type='http', auth='user', methods=['POST'], csrf=False)
    def upload_media(self, **kwargs):
        """
        Upload media file

        POST params:
            file: File upload
            storage_method: 'local' or 's3' (optional, uses config default)

        Returns:
            JSON response with media info
        """
        try:
            # Get uploaded file
            uploaded_file = request.httprequest.files.get('file')
            if not uploaded_file:
                return request.make_json_response({
                    'success': False,
                    'error': 'No file uploaded'
                }, status=400)

            # Get storage method (from param or config)
            storage_method = kwargs.get('storage_method')
            if not storage_method:
                storage_method = request.env['ir.config_parameter'].sudo().get_param(
                    'isd_marketing_template.media_storage_method', 'local'
                )

            # Read file content
            filename = secure_filename(uploaded_file.filename)
            file_content = uploaded_file.read()

            # Create media record
            media = request.env['media.library'].sudo().create_from_upload(
                filename, file_content, storage_method
            )

            return request.make_json_response({
                'success': True,
                'media': {
                    'id': media.id,
                    'name': media.name,
                    'url': media.url,
                    'file_type': media.file_type,
                    'file_size': media.file_size,
                    'storage_method': media.storage_method,
                }
            })

        except Exception as e:
            _logger.exception("Error uploading media")
            return request.make_json_response({
                'success': False,
                'error': str(e)
            }, status=500)

    @http.route('/media/file/<int:media_id>/<filename>', type='http', auth='public')
    def serve_media(self, media_id, filename, **kwargs):
        """
        Serve local media file

        Args:
            media_id (int): Media library ID
            filename (str): Filename (for SEO/clarity)

        Returns:
            File content
        """
        try:
            media = request.env['media.library'].sudo().browse(media_id)
            if not media.exists():
                return request.not_found()

            if media.storage_method != 'local':
                # Redirect to S3 URL
                return request.redirect(media.url)

            if not media.file_data:
                return request.not_found()

            # Decode file data
            file_content = base64.b64decode(media.file_data)

            # Set headers
            headers = [
                ('Content-Type', media.mime_type or 'application/octet-stream'),
                ('Content-Length', len(file_content)),
                ('Content-Disposition', f'inline; filename="{media.name}"'),
            ]

            return request.make_response(file_content, headers=headers)

        except Exception as e:
            _logger.exception(f"Error serving media {media_id}")
            return request.not_found()

    @http.route('/media/upload_multiple', type='http', auth='user', methods=['POST'], csrf=False)
    def upload_multiple_media(self, **kwargs):
        """
        Upload multiple media files

        POST params:
            files[]: Multiple file uploads
            storage_method: 'local' or 's3' (optional, uses config default)

        Returns:
            JSON response with array of media info
        """
        try:
            # Get uploaded files
            uploaded_files = request.httprequest.files.getlist('files[]')
            if not uploaded_files:
                return request.make_json_response({
                    'success': False,
                    'error': 'No files uploaded'
                }, status=400)

            # Get storage method
            storage_method = kwargs.get('storage_method')
            if not storage_method:
                storage_method = request.env['ir.config_parameter'].sudo().get_param(
                    'isd_marketing_template.media_storage_method', 'local'
                )

            # Upload all files
            media_list = []
            for uploaded_file in uploaded_files:
                try:
                    filename = secure_filename(uploaded_file.filename)
                    file_content = uploaded_file.read()

                    media = request.env['media.library'].sudo().create_from_upload(
                        filename, file_content, storage_method
                    )

                    media_list.append({
                        'id': media.id,
                        'name': media.name,
                        'url': media.url,
                        'file_type': media.file_type,
                        'file_size': media.file_size,
                        'storage_method': media.storage_method,
                    })
                except Exception as e:
                    _logger.warning(f"Failed to upload {uploaded_file.filename}: {e}")
                    media_list.append({
                        'name': uploaded_file.filename,
                        'error': str(e),
                        'success': False
                    })

            return request.make_json_response({
                'success': True,
                'media_list': media_list,
                'total': len(media_list)
            })

        except Exception as e:
            _logger.exception("Error uploading multiple media")
            return request.make_json_response({
                'success': False,
                'error': str(e)
            }, status=500)
