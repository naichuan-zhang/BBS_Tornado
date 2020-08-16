$(document).ready(function () {
    if ($('#signBtn').html() !== '登录') {
        editorRefresh()
    } else {
        $('#answer-textarea').val('您必须登录才能回答该问题')
        $('#submit-answer').attr('disabled', 'disabled')
        $('#answer-textarea').attr('readonly', 'readonly')
    }
    loadAnswers()
})

$('#submit-answer').click(function () {
    let content = $('#answer-textarea').val()
    if (!content.match('^[\\s\\S]{18,10000}$')) {
        $('#answer-editor').prepend("<div id='characterErr' style='margin-top: 10px;' class='alert alert-danger'>字符数量不符合要求</div>")
        setTimeout(function () {
            $('#characterErr').remove()
        }, 400)
        return false
    } else {
        $('#characterErr').remove()
    }
    $.ajax({
        url: '/answer/create',
        type: 'post',
        data: {
            content: content,
            qid: getCurrentQid(),
        },
        dataType: 'json',
        success: function (data) {
            if (data.status === 200 && data.data) {
                editorRefresh()
                loadAnswers()
            } else if(data.status === 200001) {
                $('#answer-editor').prepend("<div style='margin-top: 10px' class='alert alert-danger'>"+ data.message +"</div>");
            } else if(data.status === 200002 ) {
                $('#answer-editor').prepend("<div style='margin-top: 10px' class='alert alert-danger'>答案创建失败！</div>");
            } else if(data.status === 100006) {
                $('#answer-editor').prepend("<div style='margin-top: 10px' class='alert alert-danger'>"+ data.message +"</div>");
            }
        }
    })
    return false
})

function editorRefresh() {
    new Simditor({
        textarea: $('#answer-textarea'),
        placeholder: '请输入18-10000字的答案...',
        toolbarFloat: true,
        toolbarFloatOffset: 0,
        pasteImage: true,
        toolbarHidden: false,
        locale: 'zh-CN',
        toolbar: [
            'bold',
            'italic',
            'underline',
            'strikethrough',
            'fontScale',
            'color',
            'ol',
            'ul',
            'code',
            'image',
            'blockquote',
            'table',
            'link',
            'hr',
        ],
        upload: {
            url: '/question/picload',   // 文件上传的接口地址
            params: null,               // 上传时的额外参数
            fileKey: 'pic',             // 服务器端获取文件数据的参数名
            connectionCount: 3,
            leaveConfirm: '正在上传文件',
        },
    })
}

function loadAnswers() {
    let curUsername = getCookie('username')
    $('#answer_list .list-group').html('')
    $.ajax({
        url: '/answer/list/' + getCurrentQid(),
        type: 'get',
        data: {},
        dataType: 'json',
        success: function (data) {
            if (data.status === 200 && data.data) {
                let answers = data.data.answer_list
                if (answers.length) {
                    $('#notAnswer').remove()
                    let html = ""
                    for (let i in answers) {
                        if (answers[i].status) {
                            if (curUsername === answers[i].username) {
                                html += "<div class='row'>" +
                                    "<div class='col-md-2'></div>" +
                                    "<div class='col-md-10'>" +
                                    "<p style='text-align: right'><b style='font-size: 20px; color: deeppink; font-weight: 800px;'>" + answers[i].username + "</b><small>" + answers[i].created_at + "</small></p>" +
                                    "<div style='background-color: #cae1ff' class='well well-sm list-group-item'>" +
                                    "<p class='glyphicon glyphicon-ok' style='font-size: 16px; color: red;'> 已采纳</p>" +
                                    "<div class='container' style='margin-top: 20px; padding-right: 50px;'>" + answers[i].content + "</div>" +
                                    "</div>" +
                                    "</div>" +
                                    "</div><br>"
                            } else {
                                html += "<div class='row'>" +
                                    "<div class='col-md-10'>" +
                                    "<p style='text-align: left'><b style='font-size: 20px; color: deeppink; font-weight: 800px;'>" + answers[i].username + "</b><small>" + answers[i].created_at + "</small></p>" +
                                    "<div style='background-color: #cae1ff' class='well well-sm list-group-item'>" +
                                    "<p class='glyphicon glyphicon-ok' style='font-size: 16px; color: red;'> 已采纳</p>" +
                                    "<div class='container' style='margin-top: 20px; padding-right: 50px;'>" + answers[i].content + "</div>" +
                                    "</div>" +
                                    "</div>" +
                                    "<div class='col-md-2'></div>" +
                                    "</div><br>"
                            }
                        }
                    }
                    for (let i in answers) {
                        if (!answers[i].status) {
                            if (curUsername === answers[i].username) {
                                html += "<div class='row'>" +
                                    "<div class='col-md-2'></div>" +
                                    "<div class='col-md-10'>" +
                                    "<p style='text-align: right'><a id='change-answer-'" + answers[i].aid + " onclick='changeAnswer(" + answers[i].aid + ");' style='margin-right: 6px;' class='glyphicon glyphicon-pencil' href='#'></a><a style='margin-right: 6px;' id='delete-answer-" + answers[i].aid + "' onclick='deleteAnswer(" + answers[i].aid + ");' class='glyphicon glyphicon-trash' href='#'></a><b style='font-size: 18px; color: deeppink; font-weight: 800px;'>" + answers[i].username + "</b><small>" + answers[i].created_at + "</small></p>" +
                                    "<div style='background-color: #c1ffc1' class='well well-sm list-group-item'>" +
                                    "<div class='container' style='margin-top: 20px;'>" + answers[i].content + "</div>" +
                                    "</div>" +
                                    "</div>" +
                                    "</div>"
                            } else {
                                if (curUsername === $('#question-username').html()) {
                                    html += "<div class='row'><div class='col-md-12'>";
                                    html += "<p><b style='font-size: 18px;color: deeppink;font-weight: 800'>" + answers[i].username + "</b> <small>" + answers[i].created_at + "</small> <a onclick='adoptAnswer(" + answers[i].aid + ");' id='answer-adopted-" + answers[i].aid + "' style='font-size: 20px;margin-left: 10px;text-decoration: none' href='###' class='glyphicon glyphicon-heart-empty'></a></p>";
                                    html += "<div style='background-color: #fff' class='well well-sm list-group-item'>\n";
                                    html += "<div class='container' style='margin-top: 20px;padding-right:50px'>";
                                    html += answers[i].content;
                                    html += "</div>";
                                    html += "</div><div class='col-md-2'></div></div>";
                                    html += "</div><br />";
                                } else {
                                    html += "<div class='row'><div class='col-md-12'>";
                                    html += "<p><b style='font-size: 18px;color: deeppink;font-weight: 800'>" + answers[i].username + "</b> <small>" + answers[i].created_at + "</small></p>";
                                    html += "<div style='background-color: #fff' class='well well-sm list-group-item'>\n";
                                    html += "<div class='container' style='margin-top: 20px;padding-right:50px'>";
                                    html += answers[i].content;
                                    html += "</div>";
                                    html += "</div><div class='col-md-2'></div></div>";
                                    html += "</div><br />";
                                }
                            }
                        }
                    }
                    $('#answer_list .list-group').append(html)
                } else {
                    let html = "<div id='notAnswer' class='alert alert-danger'>暂无回答</div>"
                    $('#answer_list .list-group').append(html)
                }
            }
        }
    })
}

function questionChange() {
    alert('暂时不能修改')
    return false
}

function questionDelete(obj) {
    $('#deleteModal').modal('show')
    $('#confirmDelete').click(function () {
        $.ajax({
            url: '/question/delete/' + obj.id.substr(16, 21),
            type: 'post',
            data: {},
            dataType: 'json',
            success: function (data) {
                if (data.status === 200) {
                    window.location.href = '/'
                } else {
                    $('#answer_list').prepend("<div id='answer-list-message' class='alert alert-danger'>" + data.message + "</div>")
                }
            }
        })
    })
    return false
}

function changeAnswer() {
    alert('暂时不能修改')
    return false
}

function deleteAnswer(aid) {
    $('#deleteModal').modal('show')
    $('#confirmDelete').click(function () {
        $.ajax({
            url: '/answer/delete/' + aid,
            type: 'post',
            data: {
                qid: getCurrentQid(),
            },
            dataType: 'json',
            success: function (data) {
                $('#deleteModal').modal('hide')
                if (data.status === 200) {
                    $('#answer_list').prepend("<div id='answer-list-message' class='alert alert-success'>删除成功</div>")
                    setTimeout(function () {
                        $('#answer-list-message').remove()
                    }, 1000)
                } else if (data.message) {
                    $('#answer_list').prepend("<div id='answer-list-message' class='alert alert-danger'>"+ res.message +"</div>");
                   setTimeout(function () {
                       $('#answer-list-message').remove();
                   }, 1000)
                }
                location.reload()
            }
        })
    })
    return false
}

function getCurrentQid() {
    let pathname = window.location.pathname
    return pathname.match('\\d{6}$')[0]
}