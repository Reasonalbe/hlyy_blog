var subscribe = function (email) {
    my_ajax.post({
        "url": '/subscribe/',
        'data': {
            'email': email
        },
        'success': function (result) {
            if (result['code'] === 200) {
                if (result['message']) {
                    my_alert.alertSuccess(result['message'], function () {
                        window.location.reload()
                    })
                }
            }
        }
    })
};

var listenSubscribe = function() {
    var subscribe_btn = $("button[id='subscribe-btn']");

    subscribe_btn.click(function (event) {
        var email_input = $("input[name='subscribe-email']");
        var email = email_input.val();
        event.preventDefault();
        subscribe(email)
    })
}

$(function () {
    listenSubscribe();
})