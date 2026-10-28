# -*- coding: utf-8 -*-
{
    'name': 'USA Program Theme',
    'summary': 'Website theme for US education and study-abroad programs',
    'description': """
USA Program Website Theme
=========================
A full website theme: picked from Website > Configuration > Theme, it
replaces whichever theme the website was using, and picking another one
later takes it off again. Each website carries its own theme.

* Hero banner, program catalogue, five-step "How it works"
* American University Placement, About Us, Global Partner Network
* Partner call to action, plus a lookup popup and guidance form
* A home page laid out with all of the above, editable in the Builder
    """,
    # Both of these are load-bearing, not labels:
    # - the theme_ prefix is what makes Odoo store every <template> here as a
    #   theme.ir.ui.view, a pattern copied onto each website that picks the
    #   theme, rather than a view applied to every website at once
    # - the Theme category is what puts it in the theme picker, lets picking
    #   another theme take this one off, and keeps its CSS and JS off the
    #   websites that are not using it
    'category': 'Theme/Education',
    'version': '18.0.1.0.0',
    'author': 'IntelliSyncData',
    'website': 'https://intellisyncdata.com',
    'license': 'LGPL-3',
    'depends': ['website'],
    'data': [
        'views/snippets/s_usa_hero.xml',
        'views/snippets/s_usa_programs.xml',
        'views/snippets/s_usa_steps.xml',
        'views/snippets/s_usa_university.xml',
        'views/snippets/s_usa_about.xml',
        'views/snippets/s_usa_quote.xml',
        'views/snippets/s_usa_partners.xml',
        'views/snippets/s_usa_partner_cta.xml',
        'views/snippets/s_usa_modals.xml',
        'views/snippets/snippets.xml',
        'views/pages/homepage.xml',
    ],
    'assets': {
        # CSS custom properties read with var() at runtime, not SCSS variables
        # Bootstrap compiles against, so they belong here and not in
        # web._assets_primary_variables
        'web.assets_frontend': [
            'theme_usa_program/static/src/scss/css_variables.scss',
            'theme_usa_program/static/src/scss/theme_usa_program.scss',
            'theme_usa_program/static/src/js/theme_usa_program.js',
        ],
    },
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
