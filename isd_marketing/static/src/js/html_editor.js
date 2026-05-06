/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { MassMailingWysiwyg } from "@mass_mailing/js/mass_mailing_wysiwyg";
import { patch } from "@web/core/utils/patch";
import { Component, markup } from "@odoo/owl";

patch(MassMailingWysiwyg.prototype, {
    /**
     * @override
     */
    async startEdition() {
        const result = await super.startEdition(...arguments);
        this._addHTMLEditorButton();
        return result;
    },

    /**
     * Add "Edit HTML" button to snippets menu
     */
    _addHTMLEditorButton() {
        // Find the snippets menu toolbar
        const toolbar = this.snippetsMenuToolbarEl || this.toolbarEl;
        if (!toolbar) return;

        // Check if button already exists
        if (toolbar.querySelector('.o_html_editor_btn')) return;

        // Create button
        const button = document.createElement('button');
        button.className = 'btn btn-secondary o_html_editor_btn';
        button.title = _t('Edit HTML Source');
        button.innerHTML = '<i class="fa fa-code"></i> ' + _t('Edit HTML');

        button.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this._openHTMLEditor();
        });

        // Add button to toolbar
        toolbar.appendChild(button);
    },

    /**
     * Open HTML editor modal
     */
    _openHTMLEditor() {
        const editable = this.odooEditor ? this.odooEditor.editable : this.$editable[0];
        const currentHTML = editable.innerHTML;

        // Create dialog component
        class HTMLEditorDialog extends Component {
            static template = "isd_marketing.HTMLEditorDialog";
            static props = {
                html: String,
                onSave: Function,
                close: Function,
            };

            setup() {
                this.state = {
                    html: this.props.html,
                };
            }

            onSave() {
                this.props.onSave(this.state.html);
                this.props.close();
            }
        }

        this.env.services.dialog.add(HTMLEditorDialog, {
            html: currentHTML,
            onSave: (newHTML) => this._applyHTMLChanges(newHTML),
        }, {
            title: _t('Edit HTML Source'),
            size: 'xl',
        });
    },

    /**
     * Apply HTML changes to editor
     */
    _applyHTMLChanges(html) {
        const editable = this.odooEditor ? this.odooEditor.editable : this.$editable[0];
        editable.innerHTML = html;

        // Trigger history step
        if (this.odooEditor) {
            this.odooEditor.historyStep();
        }

        // Show success notification
        this.env.services.notification.add(_t('HTML code has been updated successfully'), {
            type: 'success',
        });
    },
});
