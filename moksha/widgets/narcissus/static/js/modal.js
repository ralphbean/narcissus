function loadingDialog(href) {
        var $dialog = $('<div></div>')
        .html('Loading.')
        .dialog({
                autoOpen: true,
                title: 'Narcissus',
                modal: true,
        });
        window.location.href=href
}
