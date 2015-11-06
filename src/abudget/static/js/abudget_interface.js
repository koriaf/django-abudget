(function (factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD (Register as an anonymous module)
        define(['jquery'], factory);
    // } else if (typeof exports === 'object') {
    //     // Node/CommonJS
    //     module.exports = factory(require('jquery'));
    } else {
        // Browser globals
        factory(jQuery);
    }
}(function ($) {
    $(document).bind('ready', function() {
        'use strict';
        $("#transaction_category_selector li.category_item").bind('click', function() {
            var $selected = $(this);
            $("#selected-category-field").text($selected.text());
            $("#id_selected_category").val($selected.data('category-id'));
        });

        $(".transaction-item .remove-transaction").bind('click', function() {
            if (!confirm('Sure?')) {
                return;
            }
            var $th = $(this);
            var transaction_id = $th.data('transaction-id');
            var request_payload = {
                'transaction_id': transaction_id,
                'csrfmiddlewaretoken': $.cookie('csrftoken'),
            };
            $.post("/money/transactions/remove/",  request_payload, function( data ) {
                 $th.parent('.transaction-item').fadeOut('fast');
            });
        });

        $(".transaction-item .remove-income-transaction").bind('click', function() {
            if (!confirm('Sure?')) {
                return;
            }
            var $th = $(this);
            var transaction_id = $th.data('transaction-id');
            var request_payload = {
                'transaction_id': transaction_id,
                'csrfmiddlewaretoken': $.cookie('csrftoken'),
            };
            $.post("/money/income/remove/",  request_payload, function( data ) {
                 $th.parent('.transaction-item').fadeOut('fast');
            });
        });

        $("#id_transaction_form").bind('submit', function() {
            // check if amount fiels has math expression and calculate it
            var $amount_field = $("#id_amount");
            var amount_expression = $amount_field.val().replace(',', '.');  // don't care about formats
            var result = NaN;
            try {
                result = eval(amount_expression);
            } catch (err) {
                result = NaN;
            }
            if (isNaN(result)) {
                $amount_field.css('background-color', '#faa');
                $("#id_amount").unbind('keydown');
                $("#id_amount").bind('keydown', function() {$(this).css('background-color', '')});
                return false;
            } else {
                $amount_field.val(result);
            }

            // check for all fields filled
            return true;
        });
    });
}));
