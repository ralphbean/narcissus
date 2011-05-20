function loadingDialog(href) {
        var $dialog = $('<div></div>')
        .html('Making request.')
        .dialog({
                autoOpen: true,
                title: 'Narcissus',
                modal: true,
        });
        window.location.href=href
}
