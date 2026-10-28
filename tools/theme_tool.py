#!/usr/bin/env python3
"""Check an Odoo 18 website theme before it is pushed, and build its home page.

    python tools/theme_tool.py theme_usa_program              # check only
    python tools/theme_tool.py theme_usa_program --homepage   # rebuild home page, then check

Run it with the Odoo venv's python so lxml (and libsass, for the SCSS check)
are there. Everything it checks is something that has already broken a
theme here once - see THEMES.md for why each one matters.
"""
import argparse
import ast
import os
import sys

try:
    from lxml import etree
except ImportError:
    sys.exit("lxml is missing: run this with the Odoo venv's python")

# Odoo 18's structure groups (addons/website/views/snippets/snippets.xml).
# A block with any other group, or none, has nowhere to appear in the panel.
GROUPS = {
    'intro', 'columns', 'content', 'images', 'people', 'text', 'social',
    'contact_and_forms', 'products', 'blogs', 'events', 'custom',
}

HOMEPAGE = 'views/pages/homepage.xml'
SNIPPET_DIR = 'views/snippets/'
REGISTRY = 'views/snippets/snippets.xml'

HOMEPAGE_TEMPLATE = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- The home page the theme arrives with.

         The blocks are written out in full rather than t-called. A t-call
         renders the same page, but the Website Builder cannot edit through
         one, so the page would look right and refuse to be changed. Written
         out, this becomes the website's own copy of the home page when the
         theme is applied, and is edited like any other.

         Generated from views/snippets/*.xml by tools/theme_tool.py. The two
         are expected to drift: the snippets are what can be dropped, this is
         what was dropped. Changing a snippet does not, and should not, rewrite
         a home page someone has since edited. -->
    <template id="homepage" inherit_id="website.homepage" name="{name}">
        <xpath expr="//div[@id='wrap']" position="replace">
            <div id="wrap" class="oe_structure">
{body}
            </div>
        </xpath>
    </template>
</odoo>
'''


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def read_manifest(theme_dir):
    src = open(os.path.join(theme_dir, '__manifest__.py'), encoding='utf-8').read()
    # Odoo reads the manifest with literal_eval too, so anything this rejects
    # Odoo would reject as well
    return ast.literal_eval(src[src.index('{'):src.rindex('}') + 1])


def snippet_files(manifest):
    """The snippet files in the order the manifest loads them, which is the
    order they are laid out on the home page."""
    return [f for f in manifest.get('data', [])
            if f.startswith(SNIPPET_DIR) and os.path.basename(f).startswith('s_')]


def build_homepage(theme_dir, manifest):
    sections = []
    for rel in snippet_files(manifest):
        tree = etree.parse(os.path.join(theme_dir, rel))
        for tpl in tree.iter('template'):
            if tpl.get('inherit_id'):
                continue  # layout additions such as popups, not page content
            kids = [k for k in tpl if isinstance(k.tag, str)]
            if len(kids) != 1:
                sys.exit(f"{rel}: template {tpl.get('id')} must hold exactly one root "
                         f"element, found {len(kids)}")
            node = kids[0]
            node.tail = None
            sections.append(etree.tostring(node, encoding='unicode'))

    if not sections:
        sys.exit("no snippet templates found to lay out")

    name = manifest.get('name', 'Theme') + ' Home'
    xml = HOMEPAGE_TEMPLATE.format(name=name, body='\n\n'.join(sections))
    etree.fromstring(xml.encode('utf-8'))

    path = os.path.join(theme_dir, HOMEPAGE)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(xml)
    print(f"built {HOMEPAGE}: {len(sections)} blocks")


def check(theme_dir, manifest, r):
    module = os.path.basename(os.path.normpath(theme_dir))

    # 1. The two things that make it a theme at all
    if not module.startswith('theme_'):
        r.error(f"module name '{module}' must start with theme_ - without it Odoo stores "
                f"the templates as plain views on every website, not as a theme")
    if not str(manifest.get('category', '')).startswith('Theme'):
        r.error(f"category '{manifest.get('category')}' must be Theme or Theme/... - "
                f"without it the theme is not in the picker and cannot be switched")
    if manifest.get('post_init_hook'):
        r.warn("post_init_hook set: a theme lays its pages out through templates, "
               "a hook writes into every website whether it picked the theme or not")

    # 2. Every file the manifest names exists, and every XML parses
    for rel in manifest.get('data', []):
        path = os.path.join(theme_dir, rel)
        if not os.path.exists(path):
            r.error(f"data file missing: {rel}")
            continue
        try:
            etree.parse(path)
        except etree.XMLSyntaxError as e:
            r.error(f"{rel}: {e}")
    for bundle, files in manifest.get('assets', {}).items():
        for f in files:
            rel = f.lstrip('/').split('/', 1)[1] if '/' in f.lstrip('/') else f
            if not f.lstrip('/').startswith(module + '/'):
                r.error(f"asset {f} does not start with {module}/")
            elif not os.path.exists(os.path.join(theme_dir, rel)):
                r.error(f"asset missing: {f}")
        if bundle == 'web._assets_primary_variables':
            r.warn("web._assets_primary_variables is for SCSS $variables Bootstrap "
                   "compiles against; CSS custom properties (--x) belong in assets_frontend")
    for img in manifest.get('images', []):
        if not os.path.exists(os.path.join(theme_dir, img)):
            r.error(f"image missing: {img}")

    # 3. Snippet templates and their registration line up
    templates = {}
    for rel in snippet_files(manifest):
        path = os.path.join(theme_dir, rel)
        if not os.path.exists(path):
            continue
        for tpl in etree.parse(path).iter('template'):
            if tpl.get('inherit_id'):
                continue
            templates[tpl.get('id')] = rel
            for node in tpl.iter():
                cls = node.get('class') or ''
                if 'oe_snippet_body' in cls.split():
                    r.warn(f"{rel}: oe_snippet_body on <{node.tag}> - the editor adds and "
                           f"removes it itself, Odoo's own snippets never carry it")

    reg_path = os.path.join(theme_dir, REGISTRY)
    if not os.path.exists(reg_path):
        r.error(f"{REGISTRY} missing: the blocks will not appear in the Builder panel")
    else:
        reg = etree.parse(reg_path)
        # Only the xpath expressions: the name turning up in a comment that
        # explains why not to use it is fine
        xpaths = [x.get('expr') or '' for x in reg.iter('xpath')]
        if any('o_panel_body' in x or "div[@id='snippet_structure']" in x for x in xpaths):
            r.error(f"{REGISTRY}: xpath written for Odoo 15/16 (o_panel_body / div#snippet_structure) "
                    f"- it matches nothing in 18 and the install fails. "
                    f"Use //snippets[@id='snippet_structure']")
        if "//snippets[@id='snippet_structure']" not in xpaths:
            r.error(f"{REGISTRY}: no xpath on //snippets[@id='snippet_structure']")
        registered = set()
        for t in reg.iter('t'):
            key = t.get('t-snippet')
            if not key:
                continue
            mod, _, tid = key.partition('.')
            registered.add(tid)
            if mod != module:
                r.error(f"t-snippet {key}: must be {module}.{tid}")
            if tid not in templates:
                r.error(f"t-snippet {key}: no template with id {tid}")
            if not t.get('string'):
                r.error(f"t-snippet {key}: no string= (its name in the panel)")
            group = t.get('group')
            if group not in GROUPS:
                r.error(f"t-snippet {key}: group={group!r} - must be one of {sorted(GROUPS)}")
        for tid in sorted(set(templates) - registered):
            r.warn(f"template {tid} ({templates[tid]}) is not registered in the panel")

    # 4. The home page is editable
    home = os.path.join(theme_dir, HOMEPAGE)
    if os.path.exists(home):
        if HOMEPAGE not in manifest.get('data', []):
            r.error(f"{HOMEPAGE} exists but is not in the manifest data")
        raw = open(home, encoding='utf-8').read()
        if 't-call=' in raw.split('website.homepage', 1)[-1]:
            r.error(f"{HOMEPAGE}: t-call inside the home page - it renders but the Builder "
                    f"cannot edit it. Run with --homepage to write the blocks out")
    else:
        r.warn(f"no {HOMEPAGE}: websites picking the theme keep their current home page")

    # 5. The stylesheet compiles - a failure here drops the CSS for the whole database
    try:
        import sass
    except ImportError:
        r.warn("libsass not available, SCSS not compiled - run with the Odoo venv's python")
    else:
        for files in manifest.get('assets', {}).values():
            for f in files:
                if not f.endswith('.scss'):
                    continue
                rel = f.lstrip('/').split('/', 1)[1]
                path = os.path.join(theme_dir, rel)
                if not os.path.exists(path):
                    continue
                try:
                    sass.compile(filename=path)
                except sass.CompileError as e:
                    msg = str(e).strip().splitlines()[0]
                    hint = (" - Sass computes min()/max() itself; write #{\"min(...)\"} to "
                            "hand it to the browser") if 'Incompatible units' in msg else ''
                    r.error(f"{rel}: {msg}{hint}")

    # 6. The ehub deploy names its modules by hand
    wf = os.path.join(os.path.dirname(os.path.normpath(theme_dir)) or '.',
                      '.github', 'workflows', 'ehub-demo.yml')
    if os.path.exists(wf) and module not in open(wf, encoding='utf-8').read():
        r.warn(f"{module} is not in .github/workflows/ehub-demo.yml - ehub will not get it")


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    p.add_argument('theme_dir')
    p.add_argument('--homepage', action='store_true',
                   help='rebuild views/pages/homepage.xml from the snippets first')
    args = p.parse_args()

    if not os.path.exists(os.path.join(args.theme_dir, '__manifest__.py')):
        sys.exit(f"{args.theme_dir}: no __manifest__.py")

    manifest = read_manifest(args.theme_dir)
    if args.homepage:
        build_homepage(args.theme_dir, manifest)

    r = Report()
    check(args.theme_dir, manifest, r)
    for w in r.warnings:
        print(f"  warning  {w}")
    for e in r.errors:
        print(f"  ERROR    {e}")
    if r.errors:
        sys.exit(f"{len(r.errors)} error(s): fix before pushing")
    print(f"{os.path.basename(os.path.normpath(args.theme_dir))}: OK"
          + (f" ({len(r.warnings)} warning(s))" if r.warnings else ""))


if __name__ == '__main__':
    main()
