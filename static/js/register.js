// 该function会在整个网页加载完成后再执行
$(function () {
    function bindCaptchaBtnClick() {
        $("#captcha-btn").click(function (event) {
            let $this = $(this);   // 'this' represents current button, $this represents jquery-object
            let email = $("input[name='email']").val();
            if (!email) {
                alert("Please enter your email first!");
                return;   // 没有输入邮箱则不执行后面的代码
            }
            // 取消按钮的点击事件  use off-function for cancelling certain event
            $this.off('click');

            // 发送ajax请求 (via jQuery)
            $.ajax('/auth/captcha?email='+email, {
                method: 'GET',
                success: function(result){
                    if(result['code'] == 200){
                        alert("captcha sent successfully！");
                    }else{
                        alert(result['message']);
                    }
                },
                fail: function (error){
                    console.log(error);
                }
            })

            // 倒计时 countdown
            let countdown = 6;    // 60
            let timer = setInterval(function () {
                if (countdown <= 0) {    // when countdown is over, renew captcha and clear countdown
                    $this.text('get captcha');
                    // 清掉定时器
                    clearInterval(timer);
                    // 重新绑定点击事件
                    bindCaptchaBtnClick();
                } else {
                    countdown--;
                    $this.text(countdown + "s")
                }
            }, 1000);
        })
    }
    // 倒计时结束后要恢复点击事件，即重新执行一遍本函数
    bindCaptchaBtnClick();   // 将整段函数封装成bindCaptchaBtnClick()，然后调用
});