# -*- coding: utf-8 -*-
{
    'name': 'ISD Marketing',
    'version': '19.0.0.0.0',
    'category': 'ISD Modules',
    'summary': 'Add Custom HTML Code template for Email Marketing',
    'description': """
ISD Marketing - Custom HTML Template
====================================

Adds a new email template type that allows you to write custom HTML code directly.

Features:
---------
* "HTML Code" template in Email Marketing designer
* Write your own HTML code with live preview
* Same interface as other templates (Plain Text, Newsletter, etc.)
    """,
    'author': 'ISD Development Team',
    'website': 'https://intellisyncdata.com',
    'license': 'LGPL-3',
    'depends': [
        'mass_mailing',
    ],
    'data': [
        'views/email_templates.xml',
        'views/snippet_options.xml',
    ],
    'assets': {
        'web_editor.assets_wysiwyg': [
            'isd_marketing/static/src/js/snippet_options.js',
            'isd_marketing/static/src/scss/html_editor.scss',
            'isd_marketing/static/src/xml/html_editor_dialog.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
