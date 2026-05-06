/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

const HtmlCodeWidget = publicWidget.Widget.extend({
    selector: ".s_html_code",
    disabledInEditableMode: false,

    /**
     * @override
     */
    async start() {
        this.htmlCodeEl = this.el.querySelector(".s_html_code_content");

        // Only restore HTML from data attribute when first loading (not in edit mode)
        // In edit mode, keep the current content as is
        if (this.htmlCodeEl && !this.editableMode) {
            const savedHTML = this.htmlCodeEl.getAttribute('data-html-code');
            if (savedHTML && savedHTML.trim()) {
                this.htmlCodeEl.innerHTML = savedHTML;
            }
        }

        return this._super(...arguments);
    },
});

publicWidget.registry.HtmlCode = HtmlCodeWidget;

export default HtmlCodeWidget;
