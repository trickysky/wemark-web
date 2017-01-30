(function(global) {

    var show_msg = function(level, message) {
        var msg_box = $('#msg_modal');
        msg_box.find('.modal-body>p').html(message);
        msg_box.modal('show');
    }

    global.show_msg = show_msg;

})(window);
