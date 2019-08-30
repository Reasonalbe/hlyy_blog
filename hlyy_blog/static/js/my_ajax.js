function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
// Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var my_ajax = {
    'get': function (args) {
        args['method'] = 'get';
        this.ajax(args);
    },
    'post': function (args) {
        args['method'] = 'post';
        this._ajaxSetup();
        this.ajax(args);
    },
    'ajax': function (args) {
        // args是调用ajax时传递的数据，主要参数有url,data,success,fail
        var success = args['success'];
        args['success'] = function(result) {
            if ( result['code'] !== 200) {
                //响应值不等于200，向用户提示失败原因
                var messageObj = result['message'];
                if(typeof messageObj === 'string' || messageObj.constructor === String) {
                    //返回的message是一个字符串类型
                    window.messageBox.showError(messageObj)
                } else {
                    //返回的message是一个字典类型
                    // {'password': ['XXX', 'YYY'],'telephone': ['XXX', 'YYY']}
                    for(var key in messageObj){
                        var message = messageObj[key][0];
                        message = '(' + key + ')' + message;
                        window.messageBox.showError(message)
                    }
                }
            }
            //执行调用者自己写的success函数
            if (success) {
                success(result);
            }
        };
        args['fail'] = function(error) {
            window.messageBox.showError('服务器异常，请稍后尝试')
            console.log(error)
        };

        $.ajax(args);
    },
    '_ajaxSetup':function () {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });
    }
};