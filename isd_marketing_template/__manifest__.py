# -*- coding: utf-8 -*-
{
    'name': 'ISD Marketing Template',
    'version': '18.0.1.0.0',
    'category': 'ISD Modules',
    'summary': 'Centralized email and messaging template management with HTML/CSS support',
    'description': """
ISD Marketing Template
======================
Centralized email and messaging template management system with media library.

Features:
---------
* Create and manage EMAIL templates with HTML and inline CSS
* Create and manage MESSAGE templates with plain text
* Jinja2 template engine for dynamic data binding
* Dual editor mode: WYSIWYG and Code editor
* Live preview functionality
* Module integration (e.g., isd_profile_management)
* Reusable templates across multiple modules
* CSS inlining for email compatibility
* Media Library for images and videos
* Dual storage: Local Server and AWS S3
* Easy URL copy for use in templates

Template Syntax:
---------------
* Variables: {{ object.field_name }}
* Filters: {{ value | filter_name }}
* Conditionals: {% if condition %}...{% endif %}
* Loops: {% for item in items %}...{% endfor %}

Requirements:
-------------
* Python: Pillow (included in Odoo)
* Python: boto3 (for S3 storage) - install with: pip install boto3
    """,
    'author': 'IntelliSync Data',
    'website': 'https://intellisyncdata.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'web',
        'web_editor',
    ],
    'data': [
        'wizard/media_upload_wizard_views.xml',
        'security/ir.model.access.csv',
        'views/marketing_template_views.xml',
        'views/media_library_views.xml',
        'views/res_config_settings_views.xml',
        'views/marketing_template_menus.xml',
    ],
    'external_dependencies': {
        'python': ['boto3'],
    },
    'assets': {
        'web.assets_backend': [
            'isd_marketing_template/static/src/js/template_editor.js',
            'isd_marketing_template/static/src/xml/template_editor.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
