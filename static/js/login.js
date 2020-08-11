let loginSign

$(document).ready(function () {
    refreshLoginVcode()
})

$('#loginVcode').click(function () {
    refreshLoginVcode()
})

$('#submitSignup').click(function () {
    let $username = $('#form-username')
    let $password = $('#form-password')
    let $vcode = $('#form-vcode')
    let username = $username.val()
    let password = $password.val()
    let vcode = $vcode.val()
    if (!username.match('^\\w{4,12}$')) {
        $username.css('border', 'solid red')
        $username.val('')
        $username.attr('placeholder', '用户名长度应该在4-12位之间')
        return false
    } else {
        $username.css('border', '')
    }
    if (!password.match('^\\w{6,20}$')) {
        $password.css('border', 'solid red')
        $password.val('')
        $password.attr('placeholder', '密码长度应该在6-20位之间')
        return false
    } else {
        $password.css('border', '')
    }
    if (!vcode.match('^\\w{4}$')) {
        $vcode.css('border', 'solid red')
        $vcode.val('')
        $vcode.attr('placeholder', '验证码长度为4位')
        return false
    } else {
        $vcode.css('border', '')
    }
    $.ajax({
        url: '/auth/signup',
        type: 'post',
        data: {
            username: username,
            password: password,
            vcode: vcode,
            sign: loginSign,
        },
        dataType: 'json',
        success: function (data) {
            if (data.status === 200 && data.data) {
                window.location.href = getQueryString('next') || '/' + encodeURI('?m=登录成功&e=success')
            } else if (data.status === 100001) {    // 验证码错误或超时
                $vcode.css('border', 'solid red')
                $vcode.val('')
                $vcode.attr('placeholder', data.message)
            } else if (data.status === 100004) {    // 用户名已存在
                $username.css('border', 'solid red')
                $username.val('')
                $username.attr('placeholder', data.message)
            } else if (data.status === 100005) {    // 用户创建失败
                $('.registration-form').prepend("<div id='regMessage' class='alert alert-danger'>注册失败</div>")
                setTimeout(function () {
                    $('.registration-form').find('#regMessage').remove()
                }, 1500)
            }
        }
    })
})

$('#submitLogin').click(function () {
    let $username = $('#form-username')
    let $password = $('#form-password')
    let $vcode = $('#form-vcode')
    let username = $username.val()
    let password = $password.val()
    let vcode = $vcode.val()
    if(!username.match('^\\w{4,12}$')) {
        $username.css('border', 'solid red');
        $username.val('');
        $username.attr('placeholder', '用户名长度应该在4-12位之间');
        return false;
    }else {
        $username.css('border', '');
    }
    if(!password.match('^\\w{6,20}$')) {
        $password.css('border', 'solid red');
        $password.val('');
        $password.attr('placeholder', '密码长度应该在6-20位之间');
        return false;
    }else {
        $password.css('border', '');
    }
    if(!vcode.match('^\\w{4}$')) {
        $vcode.css('border', 'solid red');
        $vcode.val('');
        $vcode.attr('placeholder', '验证码长度为4位');
        return false;
    }else {
        $vcode.css('border', '');
    }

    $.ajax({
        url: '/auth/login',
        type: 'post',
        data: {
            username: username,
            password: password,
            vcode: vcode,
            sign: loginSign,
        },
        dataType: 'json',
        success: function (data) {
            if (data.status === 200 && data.data) {
                window.location.href = getQueryString('next') || '/' + encodeURI('?m=登录成功&e=success')
            } else if (data.status === 100001) {    // 验证码错误或超时
                $vcode.css('border', 'solid red')
                $vcode.val('')
                $vcode.attr('placeholder', data.message)
            } else if (data.status === 100002) {    // 用户名错误
                $username.css('border', 'solid red')
                $username.val('')
                $username.attr('placeholder', data.message)
            } else if (data.status === 100003) {    // 密码错误
                $password.css('border', 'solid red')
                $password.val('')
                $password.attr('placeholder', data.message)
            }
        }
    })
})

function refreshLoginVcode() {
    // 更新登录验证码
    $.ajax({
        url: '/auth/v.img',
        type: 'get',
        data: {},
        dataType: 'json',
        success: function (data) {
            if (data.status === 200 && data.data) {
                $('#loginVcode').attr('src', 'data:img/png;base64,' + data.data.vcode)
                loginSign = data.data.sign
            }
        }
    })
}