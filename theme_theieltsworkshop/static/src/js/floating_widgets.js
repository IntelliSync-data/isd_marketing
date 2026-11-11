/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.TiwFloatingWidgets = publicWidget.Widget.extend({
    selector: '.tiw-floating-widgets',
    events: {
        'click .btn-scroll-top': '_onScrollToTop',
    },

    start: function () {
        const self = this;
        this.$scrollTopBtn = this.$('.btn-scroll-top');
        
        $(window).on('scroll.tiw_floating', function () {
            if ($(window).scrollTop() > 400) {
                self.$scrollTopBtn.removeClass('d-none');
            } else {
                self.$scrollTopBtn.addClass('d-none');
            }
        });

        return this._super.apply(this, arguments);
    },

    destroy: function () {
        $(window).off('scroll.tiw_floating');
        this._super.apply(this, arguments);
    },

    _onScrollToTop: function (ev) {
        ev.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    },
});

export default publicWidget.registry.TiwFloatingWidgets;

