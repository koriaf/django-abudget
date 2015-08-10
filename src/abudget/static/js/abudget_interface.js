// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie != '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// };

$(document).bind('ready', function() {
    'use strict';
    $("#transaction_category_selector li.category_item").bind('click', function() {
        var $selected = $(this);
        $("#selected-category-field").text($selected.text());
        $("#id_selected_category").val($selected.data('category-id'));
    });

    $(".transaction-item .remove-transaction").bind('click', function() {
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
});
