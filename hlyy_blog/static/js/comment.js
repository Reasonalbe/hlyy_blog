function Comment() {

}

Comment.prototype.listenCommentSubmit = function() {
    var self = this;
    var submitBtn = $("#submit_btn");
    submitBtn.click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        var post_id = $("input[name='submit_btn']").attr("data-post-id");
        var nickname = $("input[name='nickname']").val();
        var content = $("textarea[name='content']").val();
        var captcha = $("input[id='id_captcha_1']").val();
        if (email) {
            my_alert.alertConfirm({
                'text': '是否通过邮箱订阅该博客？',
                'confirmCallback': function () {
                     my_ajax.post({
                        "url": '/comment/',
                        'data': {
                            'email': email,
                            'post_id': post_id,
                            'nickname': nickname,
                            'content': content,
                            'captcha': captcha,
                        },
                        'success': function (result) {
                            if (result['code'] === 200) {
                                window.messageBox.showSuccess('评论成功！')
                                window.location.reload()
                            }
                        }
                    })
                },
                'cancelCallback': function () {
                    my_ajax.post({
                        "url": '/comment/',
                        'data': {
                            'nickname': nickname,
                            'content': content,
                            'captcha': captcha,
                        },
                        'success': function (result) {
                            if (result['code'] === 200) {
                                window.messageBox.showSuccess('评论成功！')
                                window.location.reload()
                            }
                        }
                    })
                    my_alert.close();
                }
            })
        } else {
            my_ajax.post({
                "url": '/comment/',
                'data': {
                    'nickname': nickname,
                    'content': content,
                    'captcha': captcha,
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        window.messageBox.showSuccess('评论成功！')
                        window.location.reload()
                    }
                }
            })
        }

    })
};

Comment.prototype.listenRefreshCaptcha = function(){
    var captcha = $("#comment-submit-form img[class='captcha']")
    captcha.click(function () {
        $.get("/captcha/refresh/?"+Math.random(), function(result){
            captcha.attr("src",result.image_url);
            captcha.attr("value",result.key);
        });
        return false;
    })
}

Comment.prototype.run = function () {
    this.listenCommentSubmit();
    this.listenRefreshCaptcha();
};

$(function () {
    var comment = new Comment();
    comment.run();
});