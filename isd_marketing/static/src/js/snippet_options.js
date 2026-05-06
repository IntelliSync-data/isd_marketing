/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import options from "@web_editor/js/editor/snippets.options";
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

/**
 * Clone HTML string to DOM elements
 */
function cloneContentEls(html) {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    return Array.from(tempDiv.childNodes);
}

/**
 * HTML Code Editor Dialog Component
 */
class HTMLCodeEditorDialog extends Component {
    static template = "isd_marketing.HTMLCodeEditorDialog";
    static components = { Dialog };
    static props = {
        title: String,
        value: String,
        confirm: Function,
        close: Function,
    };

    setup() {
        this.state = useState({
            value: this.props.value,
        });
    }

    onConfirm() {
        this.props.confirm(this.state.value);
        this.props.close();
    }
}

/**
 * HTML Code Block Options
 */
options.registry.HtmlCodeBlock = options.Class.extend({
    init() {
        this._super(...arguments);
        this.dialog = this.bindService("dialog");
    },

    /**
     * @override
     */
    _computeWidgetState(methodName, params) {
        if (methodName === 'editHtmlCode') {
            return '';
        }
        return this._super(...arguments);
    },

    /**
     * Edit HTML Code button handler
     */
    async editHtmlCode(previewMode, widgetValue, params) {
        // Ignore preview mode - only execute on real click
        if (previewMode) {
            return;
        }

        const $container = this.$target.find('.s_html_code_content');

        // Always get current HTML from the actual content (what user sees)
        const currentHTML = $container[0].innerHTML;

        await new Promise(resolve => {
            this.dialog.add(HTMLCodeEditorDialog, {
                title: _t("Edit HTML Code"),
                value: currentHTML.trim(),
                confirm: (newHTML) => {
                    // Get the wysiwyg/odooEditor instance
                    const odooEditor = this.options.wysiwyg.odooEditor;

                    // Wrap the change in a history step so Odoo doesn't undo it
                    if (odooEditor) {
                        odooEditor.observerUnactive('editHtmlCode');
                        $container[0].innerHTML = newHTML;
                        odooEditor.observerActive('editHtmlCode');
                        odooEditor.historyStep();
                    } else {
                        // Fallback if no odooEditor
                        $container[0].innerHTML = newHTML;
                    }
                }
            }, {
                onClose: resolve,
            });
        });
    },
});

export default {
    HtmlCodeBlock: options.registry.HtmlCodeBlock,
};
