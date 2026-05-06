# -*- coding: utf-8 -*-
import logging
from jinja2 import Template, TemplateSyntaxError
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class MarketingTemplate(models.Model):
    _name = 'marketing.template'
    _description = 'Marketing Email/Message Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Basic Information
    name = fields.Char(
        string='Template Name',
        required=True,
        tracking=True,
        help='Internal name for this template'
    )

    template_type = fields.Selection([
        ('email', 'Email (HTML with inline CSS)'),
        ('message', 'Message (Plain Text)')
    ], string='Type', required=True, default='email', tracking=True)

    active = fields.Boolean(string='Active', default=True, tracking=True)

    # Module Integration
    module_reference = fields.Selection([
        ('isd_profile_management', 'Profile Management'),
        ('general', 'General'),
    ], string='Related Module', default='general', help='Module that uses this template')

    # Template Content
    subject = fields.Char(
        string='Subject',
        help='Email subject line (supports Jinja2 variables)'
    )

    content_html = fields.Html(
        string='HTML Content',
        help='HTML content with inline CSS for email templates'
    )

    content_text = fields.Text(
        string='Text Content',
        help='Plain text content for message templates'
    )

    # Editor Mode
    editor_mode = fields.Selection([
        ('wysiwyg', 'WYSIWYG Editor'),
        ('code', 'Code Editor')
    ], string='Editor Mode', default='wysiwyg', help='Switch between visual and code editor')

    # CSS Inlining
    auto_inline_css = fields.Boolean(
        string='Auto Inline CSS',
        default=True,
        help='Automatically inline CSS styles for email compatibility'
    )

    content_inlined = fields.Html(
        string='Inlined Content',
        compute='_compute_content_inlined',
        store=True,
        help='Content with CSS inlined (computed)'
    )

    # Preview
    preview_html = fields.Html(
        string='Preview',
        compute='_compute_preview_html',
        help='Preview of rendered template with sample data'
    )

    # Variables
    available_variables = fields.Text(
        string='Available Variables',
        compute='_compute_available_variables',
        help='List of available Jinja2 variables for this template'
    )

    # Metadata
    usage_count = fields.Integer(
        string='Usage Count',
        default=0,
        help='Number of times this template has been used'
    )

    last_used_date = fields.Datetime(
        string='Last Used',
        readonly=True,
        help='Last time this template was used'
    )

    notes = fields.Text(string='Notes', help='Internal notes about this template')

    # API Integration
    api_key = fields.Char(
        string='API Key',
        help='API key for external integrations to send emails using this template',
        copy=False,
        readonly=True
    )

    api_enabled = fields.Boolean(
        string='Enable API Access',
        default=False,
        help='Allow external systems to send emails using this template via API'
    )

    @api.depends('content_html', 'auto_inline_css')
    def _compute_content_inlined(self):
        """Compute inlined CSS content"""
        for record in self:
            if record.template_type == 'email' and record.content_html and record.auto_inline_css:
                try:
                    # TODO: Implement CSS inlining using premailer or similar
                    # For now, just return the original content
                    record.content_inlined = record.content_html
                except Exception as e:
                    _logger.warning(f"Failed to inline CSS for template {record.name}: {e}")
                    record.content_inlined = record.content_html
            else:
                record.content_inlined = record.content_html or ''

    @api.depends('content_html', 'content_text', 'template_type', 'subject')
    def _compute_preview_html(self):
        """Generate preview with sample data"""
        for record in self:
            sample_data = record._get_sample_data()
            try:
                if record.template_type == 'email':
                    rendered_html = record.render_template(sample_data)
                    record.preview_html = f"""
                        <div style="border: 1px solid #ccc; padding: 20px; background: #f9f9f9;">
                            <div style="background: white; padding: 20px; border-radius: 4px;">
                                <h4 style="margin: 0 0 10px 0; color: #555;">Subject: {record.subject or '(No subject)'}</h4>
                                <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">
                                {rendered_html}
                            </div>
                        </div>
                    """
                else:
                    rendered_text = record.render_template(sample_data)
                    record.preview_html = f"""
                        <div style="border: 1px solid #ccc; padding: 20px; background: #f9f9f9;">
                            <pre style="background: white; padding: 20px; border-radius: 4px; white-space: pre-wrap;">{rendered_text}</pre>
                        </div>
                    """
            except Exception as e:
                record.preview_html = f"""
                    <div style="color: red; padding: 20px; border: 1px solid red; background: #fff0f0;">
                        <strong>Error rendering preview:</strong><br/>
                        {str(e)}
                    </div>
                """

    @api.depends('module_reference')
    def _compute_available_variables(self):
        """Compute available variables based on module"""
        for record in self:
            variables = []

            # Common variables available in all templates
            variables.append("# Common Variables:")
            variables.append("{{ object }} - Main record object")
            variables.append("{{ company.name }} - Company name")
            variables.append("{{ company.email }} - Company email")
            variables.append("{{ user.name }} - Current user name")

            # Module-specific variables
            if record.module_reference == 'isd_profile_management':
                variables.append("\n# Profile Management Variables:")
                variables.append("{{ object.name }} - Payment reference")
                variables.append("{{ object.user_id.name }} - User name")
                variables.append("{{ object.user_id.email }} - User email")
                variables.append("{{ object.amount }} - Payment amount")
                variables.append("{{ object.transaction_id }} - Transaction ID")
                variables.append("{{ object.qr_url }} - QR code URL")
                variables.append("{{ object.state }} - Payment state")

            record.available_variables = "\n".join(variables)

    def _get_sample_data(self):
        """Get sample data for preview"""
        self.ensure_one()

        # Create sample context
        sample_data = {
            'object': {
                'name': 'PAY00001',
                'user_id': {'name': 'John Doe', 'email': 'john.doe@example.com'},
                'amount': 2000000,
                'transaction_id': 'TEST_ABC123',
                'qr_url': 'https://example.com/qr-code.png',
                'state': 'pending',
            },
            'company': {
                'name': self.env.company.name,
                'email': self.env.company.email or 'info@company.com',
            },
            'user': {
                'name': self.env.user.name,
            }
        }

        return sample_data

    def render_template(self, data):
        """Render template with given data using Jinja2

        Args:
            data (dict): Context data for rendering

        Returns:
            str: Rendered template
        """
        self.ensure_one()

        if self.template_type == 'email':
            content = self.content_inlined or self.content_html or ''
        else:
            content = self.content_text or ''

        if not content:
            return ''

        try:
            # Render using Jinja2
            template = Template(content)
            rendered = template.render(**data)
            return rendered
        except TemplateSyntaxError as e:
            raise ValidationError(_(f"Template syntax error: {str(e)}"))
        except Exception as e:
            raise ValidationError(_(f"Error rendering template: {str(e)}"))

    def render_subject(self, data):
        """Render subject line with given data

        Args:
            data (dict): Context data for rendering

        Returns:
            str: Rendered subject
        """
        self.ensure_one()

        if not self.subject:
            return ''

        try:
            template = Template(self.subject)
            rendered = template.render(**data)
            return rendered
        except Exception as e:
            _logger.warning(f"Error rendering subject for template {self.name}: {e}")
            return self.subject

    def action_preview(self):
        """Open preview wizard"""
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': _('Template Preview - %s') % self.name,
            'res_model': 'marketing.template.preview.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_template_id': self.id},
        }

    def action_duplicate(self):
        """Duplicate template"""
        self.ensure_one()

        new_template = self.copy({'name': f"{self.name} (Copy)"})

        return {
            'type': 'ir.actions.act_window',
            'name': _('Template'),
            'res_model': 'marketing.template',
            'res_id': new_template.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_usage(self):
        """View usage statistics (placeholder)"""
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Template Usage'),
                'message': _('This template has been used %s times. Last used: %s') % (
                    self.usage_count,
                    self.last_used_date.strftime('%Y-%m-%d %H:%M') if self.last_used_date else _('Never')
                ),
                'type': 'info',
                'sticky': False,
            }
        }

    def increment_usage(self):
        """Increment usage counter"""
        self.ensure_one()
        self.write({
            'usage_count': self.usage_count + 1,
            'last_used_date': fields.Datetime.now(),
        })

    def action_generate_api_key(self):
        """Generate new API key for this template"""
        self.ensure_one()
        import secrets
        api_key = f"mt_{self.id}_{secrets.token_urlsafe(32)}"
        self.write({'api_key': api_key})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('API Key Generated'),
                'message': _('New API key has been generated successfully'),
                'type': 'success',
                'sticky': False,
            }
        }

    def send_email_via_api(self, recipient_email, variables=None):
        """Send email using this template (called by API)

        Args:
            recipient_email (str): Recipient email address
            variables (dict): Variables to render in template

        Returns:
            dict: Result with success status
        """
        self.ensure_one()

        if self.template_type != 'email':
            raise ValidationError(_("This template is not an email template"))

        if not variables:
            variables = {}

        # Add recipient to variables
        variables.setdefault('recipient', {'email': recipient_email})

        # Render template and subject
        rendered_content = self.render_template(variables)
        rendered_subject = self.render_subject(variables)

        # Send email
        mail_values = {
            'subject': rendered_subject or self.name,
            'body_html': rendered_content,
            'email_to': recipient_email,
            'email_from': self.env.company.email or self.env.user.email,
            'auto_delete': True,
        }

        mail = self.env['mail.mail'].sudo().create(mail_values)
        mail.send()

        # Increment usage
        self.increment_usage()

        return {
            'success': True,
            'mail_id': mail.id,
            'message': _('Email sent successfully to %s') % recipient_email
        }

    @api.constrains('subject')
    def _check_subject_for_email(self):
        """Validate that email templates have a subject"""
        for record in self:
            if record.template_type == 'email' and not record.subject:
                raise ValidationError(_("Email templates must have a subject line."))

    @api.constrains('content_html', 'content_text')
    def _check_content(self):
        """Validate that template has content"""
        for record in self:
            if record.template_type == 'email' and not record.content_html:
                raise ValidationError(_("Email templates must have HTML content."))
            if record.template_type == 'message' and not record.content_text:
                raise ValidationError(_("Message templates must have text content."))
