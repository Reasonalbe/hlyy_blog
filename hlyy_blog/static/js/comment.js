function Comment() {

}

Comment.prototype.listenCommentSubmit = function() {
    var comment_submitBtn = $("#comment_form button[name='submit_btn']");
    var reply_submitBtn = $("#reply_form button[name='submit_btn']");
    var click_function = function (form) {
        var post_id = form.find("button[name='submit_btn']").data('post-id');
        var nickname = form.find("input[name='nickname']").val();
        var content = form.find("textarea[name='content']").val();
        var captcha = form.find("input[name='captcha']").val();
        var email = form.find("input[name='email']").val();
        var url = form.find("input[name='url']").val();
        var hashkey = form.find("input[name='hashkey']").val();
        var reply_comment_id =form.find("input[name='reply_comment_id']").val();
        my_ajax.post({
            "url": '/comment/',
            'data': {
                'nickname': nickname,
                'content': content,
                'captcha': captcha,
                'hashkey': hashkey,
                'post_id': post_id,
                'email': email,
                'url': url,
                'reply_comment_id': reply_comment_id,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    my_alert.alertSuccess('评论成功！', function () {
                        window.location.reload()
                    })

                }
            }
        })
    };
    comment_submitBtn.click(function (event) {
        event.preventDefault();
        form = $("#comment_form");
        click_function(form);
    })
    reply_submitBtn.click(function (event) {
        event.preventDefault();
        form = $("#reply_form");
        click_function(form);
    })

};

Comment.prototype.listenRefreshCaptcha = function(){
    var captcha = $("img[class='captcha']");
    var hashkey = $("input[name='hashkey']");
    captcha.click(function () {
        $.get("/captcha/refresh/?"+Math.random(), function(result){
            captcha.attr("src",result.image_url);
            captcha.attr("value",result.key);
            hashkey.attr("value",result.key);
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

$('#replyModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var comment_id = button.data('comment-id') // Extract info from data-* attributes
    var nickname = button.data('nickname') // Extract info from data-* attributes
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)
    modal.find('.modal-title').text('回复 ' + nickname)
    modal.find('input[name="reply_comment_id"]').val(comment_id)
});

$(function (){
    $("[data-toggle='popover']").popover({
        trigger: 'focus'
    });
});
