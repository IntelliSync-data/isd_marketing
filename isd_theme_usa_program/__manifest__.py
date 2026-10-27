# -*- coding: utf-8 -*-
{
    'name': 'USA Program Theme (by ISD)',
    'summary': 'Website theme for US education and study-abroad programs',
    'description': """
USA Program Website Theme
=========================
Drag-and-drop blocks for an international education site:

* Hero banner, program catalogue, five-step "How it works"
* American University Placement, About Us, Global Partner Network
* Partner call to action, plus a lookup popup and guidance form
* Bootstrap 5, laid out for phone, tablet and desktop

Installing lays the blocks out on an empty home page. A home page that
already has content is left alone - the blocks are in the Website Builder
panel under Structure.
    """,
    # Not Theme/*: Odoo treats anything under that category as a real theme,
    # and picking one in Website > Configuration > Theme uninstalls whichever
    # theme is active first. This module carries no theme.ir.ui.view records,
    # so that trade would cost the site its actual theme and give nothing
    # back. It is a set of blocks, and installs from Apps like one.
    'category': 'Website',
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
    ],
    'assets': {
        # The brand colours are CSS custom properties, not SCSS variables, so
        # they belong here and not in web._assets_primary_variables: nothing
        # is compiled against them, the stylesheet reads them with var() at
        # runtime. The file name used to say primary_variables, which is what
        # that other bundle is for, and it invites exactly that mistake.
        'web.assets_frontend': [
            'isd_theme_usa_program/static/src/scss/css_variables.scss',
            'isd_theme_usa_program/static/src/scss/isd_theme_usa_program.scss',
            'isd_theme_usa_program/static/src/js/isd_theme_usa_program.js',
        ],
    },
    'images': [
        'static/description/icon.png',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
}
