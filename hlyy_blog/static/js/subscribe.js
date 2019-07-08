var listenSubscribeBtnClick = function() {
    var subscribe_btn = $("a#subscribe_btn");
    subscribe_btn.click(function () {
        my_ajax.get({
            'url': '/subscribe/',
            'success': function (result) {
                if (result['code'] === 200) {
                    my_alert.alertSuccess('邮件发送成功！')
                }
            }
        })
    })
}

$(function () {
    listenSubscribeBtnClick();
})