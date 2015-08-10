$(document).bind('ready', function() {
    'use strict';
    $("#transaction_category_selector li.category_item").bind('click', function() {
        var $selected = $(this);
        $("#selected-category-field").text($selected.text());
        $("#id_selected_category").val($selected.data('category-id'));
    });
});
