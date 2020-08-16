$('#search-user').on('keyup', function (event) {
    if (event.keyCode === 13) {
        console.log('ENTER ...')
        let s = $(this).val()
        if (!s.match('\\w{2,12}')) {
            $(this).val('')
            $(this).css('border', '1px solid red')
            $(this).attr('placeholder', '用户名应该在2-12位之间的字母数字下划线')
            return false
        } else {
            $(this).val('')
            $(this).css('border', '')
            $(this).attr('placeholder', '查询用户')
        }
        $.ajax({
            url: '/user/search?s=' + s,
            type: 'get',
            data: {},
            dataType: 'json',
            success: function (data) {
                if (data.status === 200 && data.data) {
                    let userList = data.data.user_list
                    let html = ""
                    for (let i in userList) {
                        html += "<div class='list-group-item list-group-item-success'>" +
                            "<b style='color: red;'>" + userList[i].rank + "</b>" +
                            "<b style='margin-left: 20px; font-size: 20px;'>" + userList[i].username + "</b>" +
                            "<b style='float: right;'><span style='color: red;'>" + userList[i].point + "</span> 金</b>" +
                            "</div>"
                    }
                    $('#user-list').html(html)
                } else {
                    alert(data.message)
                }
            }
        })
    }
})