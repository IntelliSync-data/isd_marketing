# -*- coding: utf-8 -*-
import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

# The order they are laid out on the page, which is also the order they read in
SNIPPETS = [
    's_usa_hero',
    's_usa_programs',
    's_usa_steps',
    's_usa_university',
    's_usa_about',
    's_usa_quote',
    's_usa_partners',
    's_usa_partner_cta',
]


def post_init_hook(env):
    """Lay the blocks out on the home page, once, at install.

    The alternative was a template that t-calls each snippet. That renders,
    but the Website Builder cannot edit through a t-call, so the page would
    look right and refuse to be changed. Rendering here writes plain markup
    instead - the same thing dropping the blocks by hand would leave behind -
    so everything stays editable afterwards.

    A home page someone has already worked on is left alone. Arriving with a
    theme is no reason to throw away what is there, and the blocks are in the
    Builder panel for whoever wants them.
    """
    if not isinstance(env, api.Environment):  # Odoo < 17 passed (cr, registry)
        env = api.Environment(env, SUPERUSER_ID, {})

    try:
        body = ''.join(
            env['ir.qweb']._render('isd_theme_usa_program.%s' % name)
            for name in SNIPPETS
        )
    except Exception:
        _logger.exception(
            "isd_theme_usa_program: could not render the blocks, "
            "home page left as it was. Drag them in from the Builder instead.")
        return

    arch = (
        '<t t-call="website.layout">'
        '<t t-set="pageName" t-value="\'homepage\'"/>'
        '<div id="wrap" class="oe_structure">%s</div>'
        '</t>' % body
    )

    homepage = env.ref('website.homepage', raise_if_not_found=False)
    if not homepage:
        _logger.warning("isd_theme_usa_program: no website.homepage to write to")
        return

    for website in env['website'].search([]):
        view = homepage.with_context(website_id=website.id)
        if not _is_empty(view.arch_db or ''):
            _logger.info(
                "isd_theme_usa_program: home page of %s already has content, "
                "leaving it alone", website.name)
            continue
        # website_id in the context is what makes Odoo copy the view for this
        # website rather than edit the one every website shares
        view.write({'arch_db': arch})
        _logger.info("isd_theme_usa_program: laid the blocks out on %s", website.name)


def _is_empty(arch):
    """A home page nobody has put anything on yet.

    The one Odoo ships carries oe_empty and an unclosed wrap; anything else
    means a person has been here.
    """
    return 'oe_empty' in arch or '<div id="wrap" class="oe_structure"/>' in arch
