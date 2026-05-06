/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

/**
 * Client action to copy text to clipboard
 */
async function copyToClipboard(env, action) {
    const text = action.params.text;

    try {
        await navigator.clipboard.writeText(text);
        env.services.notification.add(_t("URL copied to clipboard!"), {
            type: "success",
        });
    } catch (err) {
        // Fallback for older browsers
        const textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            env.services.notification.add(_t("URL copied to clipboard!"), {
                type: "success",
            });
        } catch (err2) {
            env.services.notification.add(_t("Failed to copy URL"), {
                type: "danger",
            });
        }
        document.body.removeChild(textArea);
    }
}

registry.category("actions").add("copy_to_clipboard", copyToClipboard);

console.log("ISD Marketing Template JS loaded");
