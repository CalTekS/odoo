/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.CheckPrivateInfoWidget = publicWidget.Widget.extend({
    selector: '#wrapwrap', 
    start: function () {
        this._super.apply(this, arguments);
        this._checkProfileStatus();
    },

    _checkProfileStatus: async function () {
        try {
            const result = await rpc('/web/dataset/call_kw', {
                model: 'hr.employee',
                method: 'check_my_private_info',
                args: [],
                kwargs: {},
            });

            if (result && result.is_incomplete) {
                const $modal = $('#privateInfoModal');
                
                if ($modal.length) {
                    $modal.find('#profileUpdateButton').attr('href', result.url);

                    const $list = $modal.find('#missingFieldsList');
                    $list.empty(); 

                    result.missing_fields.forEach(function (field) {
                        $list.append('<li><i class="fa fa-exclamation-triangle me-2"></i>' + field + '</li>');
                    });
                    
                    $modal.modal({
                        backdrop: 'static',
                        keyboard: false
                    });
                    $modal.modal('show');
                }
            }
        } catch (error) {
            console.error("Error validando la información privada:", error);
        }
    },
});