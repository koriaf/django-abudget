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
    function transaction_category_select_click() {
        var $selected = $(this);
        $("#selected-category-field").text($selected.text());
        $("#id_selected_category").val($selected.data('category-id'));
    }

    function transaction_item_remove_btn_click(trans_id) {
        console.log(arguments);
        if (!confirm('Are you sure about removing this transaction?')) {
            return;
        }
        var $th = $(this);
        var transaction_id = $th.data('transaction-id');
        var request_payload = {
            'transaction_id': transaction_id,
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
        };
        $.post("/money/transactions/remove/",  request_payload, function( data ) {
            // todo: error handling (quite small possibility of error here)
            $th.parent('.transaction-item').fadeOut('fast');
        });
    }

    function transaction_form_submit() {
        // submit transaction form: ajax transaction create view
        var $form = $(this);
        // check if amount fiels has math expression and calculate it if it's possible,
        // show error otherwise - we assume that any numeric amount always possible to calculate
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
        // do ajax request to create transaction
        var data = $form.serialize();
        $.ajax({
            type: "POST",
            url: $form.attr('action'),
            data: data,
            success: function(data){
                if (data.status == 'success') {
                    // fine.
                    var $trans_container = $("#id_transactions_list");
                    var new_trans = data.data;
                    // todo: remove HTML code duplicate
                    var div_tpl = `<div class='transaction-item row'>
                        <i class='remove-transaction fa fa-times-circle' data-transaction-id='${new_trans.id}'></i>
                        <span class='category col-lg-6'>${new_trans.category}</span>
                        <span class='amount col-lg-3'>${new_trans.amount}</span>
                        <span class='date col-lg-2'>just now</span>
                        <span class='title col-lg-12'>${new_trans.title}</span>
                    </div>`;
                    $trans_container.prepend(div_tpl);
                    $(".transaction-item .remove-transaction").bind('click', transaction_item_remove_btn_click);
                    // clear form fields
                    $form.find('input[name="amount"]').val('');
                    $form.find('input[name="title"]').val('');
                } else {
                    alert(data.message);
                } 
            },
            dataType: 'json'
        });
        // check for all fields filled
        return false;
    };

    $(document).bind('ready', function() {
        'use strict';

        // select category from categories list to add transaction with it
        $("#transaction_category_selector li.category_item").bind('click', transaction_category_select_click);

        // remove transaction button (cross in red circle on each transaction row)
        $(".transaction-item .remove-transaction").bind('click', transaction_item_remove_btn_click);

        // remote income transaction button
        $(".transaction-item .remove-income-transaction").bind('click', function() {
            if (!confirm('Are you sure about removing this income?')) {
                return;
            }
            var $th = $(this);
            var transaction_id = $th.data('transaction-id');
            var request_payload = {
                'transaction_id': transaction_id,
                'csrfmiddlewaretoken': $.cookie('csrftoken'),
            };
            $.post("/money/income/remove/",  request_payload, function( data ) {
                // todo: error handling, remove duplicate code with just transaction removal
                $th.parent('.transaction-item').fadeOut('fast');
            });
        });

        $("#id_transaction_form").bind('submit', transaction_form_submit);
    });
}));
