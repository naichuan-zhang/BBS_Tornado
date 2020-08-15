let lastQid

$(document).ready(function () {
    loadQuestionList(0)
})

$('#nextQuestions').click(function () {
    loadQuestionList(0, lastQid)
})

$('#preQuestions').click(function () {
    loadQuestionList(1, lastQid)
})

function loadQuestionList(pre, last_qid) {
    $.ajax({
        url: '/question/list',
        type: 'get',
        data: {
            pre: pre,
            lqid: last_qid,
        },
        dataType: 'json',
        success: function(data) {
            if (data.status === 200 && data.data) {
                let list = data.data.question_list
                if (list.length) {
                    let html = ""
                    for (let item in list) {
                        html += "<a style='text-align: left;' class='list-group-item' href='/question/detail/" + list[item].qid + "'>" +
                            "<span>" + list[item].abstract + "</span>" +
                            "<span style='float: right; margin-right: 25px;' class='glyphicon glyphicon-pencil'>" + list[item].answer_count + "</span>" +
                            "<span style='float: right; margin-right: 25px;' class='glyphicon glyphicon-eye-open'>" + list[item].view_count + "</span>" +
                            "<span style='float: right; margin-right: 25px;' class='glyphicon glyphicon-user'>" + list[item].username + "</span>" +
                            "</a>"
                    }
                    $('#question-list').html(html)
                    lastQid = data.data.last_qid
                } else {
                    $('#question-list').prepend("<div id='pageMessage' class='alert alert-danger'>没有更多了</div>")
                    setTimeout(function () {
                        $('#question-list').find('#pageMessage').remove()
                    }, 1000)
                }
            }
        }
    })
}

$('#search-btn').click(function () {
    searchQuestion('#search')
})

$('#result-search-btn').click(function () {
    searchQuestion('#result-search')
})

function searchQuestion(input) {
    let search = $(input).val()
    if (!search.match('^[\\s\\S]{4,14}')) {
        $(input).css('border', 'solid red')
        $(input).val('')
        $(input).attr('placeholder', '关键字不能少于4个字符大于14个字符')
        return false
    } else {
        $(input).css('border', '')
    }
    window.location.href = '/question/search?s=' + search
}

$('#newest').click(function () {
    loadQuestionListByFilter('newest')
    console.log('newest')
})

$('#hotest').click(function () {
    loadQuestionListByFilter('hotest')
    console.log('hotest')
})

$('#under').click(function () {
    loadQuestionListByFilter('under')
})

$('#hasdone').click(function () {
    loadQuestionListByFilter('hasdone')
})

$('#prefer').click(function () {
    loadQuestionListByFilter('prefer')
})

function filterTag(obj) {
    loadQuestionListByFilter(obj.id)
    return false
}

function loadQuestionListByFilter(name) {
    $.ajax({
        url: '/question/filter/' + name,
        type: 'get',
        data: {},
        dataType: 'json',
        success: function(data) {
            if (data.status === 200 && data.data) {
                let list = data.data.question_list
                let html = ""
                for (let item in list) {
                    html += "<a style='text-align: left;' class='list-group-item' href='/question/detail/" + list[item].qid + "'>" +
                            "<span>" + list[item].abstract + "</span>" +
                            "<span style='float: right; margin-right: 25px;' class='glyphicon glyphicon-pencil'>" + list[item].answer_count + "</span>" +
                            "<span style='float: right; margin-right: 25px;' class='glyphicon glyphicon-eye-open'>" + list[item].view_count + "</span>" +
                            "<span style='float: right; margin-right: 25px;' class='glyphicon glyphicon-user'>" + list[item].username + "</span>" +
                            "</a>"
                }
                $('#question-list').html(html)
                $('#preQuestions').attr('disabled', 'disabled')
                $('#nextQuestions').attr('disabled', 'disabled')
            }
        }
    })
}

$('#refreshQ').click(function () {
    loadQuestionList()
    $('#preQuestions').removeAttr('disabled')
    $('#nextQuestions').removeAttr('disabled')
})
