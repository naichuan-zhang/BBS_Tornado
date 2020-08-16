let editor = new Simditor({
    textarea: $('#question-content'),
    placeholder: '请输入18-10000字的详细描述...',
    toolbarFloat: true,
    toolbarFloatOffset: 0,
    cleanPaste: true,
    pasteImage: true,
    toolbarHidden: false,
    toolbar: [
        'title',
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
        'indent',
        'outdent',
        'alignment',
    ],
    upload: {
        url: '/question/picload',
        params: null,
        fileKey: 'pic',
        connectionCount: 3,
        leaveConfirm: '正在上传文件...'
    }
})

$('#submit-question').click(function () {
    let abstract = $('#question-abstract').val()
    let content = $('#question-content').val()
    console.log(content)
    let tag_id = $('#question-tag').find('option:selected').attr('id')
    if (!abstract.match('^[\\s\\S]{7,40}$')) {
        $('#question-abstract').css('border', 'solid red')
        $('#editorForm').prepend("<div id='absMessage' class='alert alert-danger'>简述长度不符合要求</div>")
        setTimeout(function () {
            $('#absMessage').remove()
        }, 1000)
        return false;
    } else {
        $('#absMessage').remove();
        $('#question-abstract').css('border', '');
    }
    if(!content.match('^[\\s\\S]{1,102400}$')){
        $('#textareaForm').css('border', '1px solid red');
        $('#editorForm').prepend("<div id='absMessage' class='alert alert-danger'>问题描述不符合长度</div>");
        setTimeout(function () {
            $('#absMessage').remove();
        }, 1000);
        return false;
    } else {
        $('#question-content').css('border', '');
    }
    $.ajax({
        url: '/question/create',
        type: 'post',
        data: {
            abstract: abstract,
            content: content,
            tag_id: tag_id,
        },
        dataType: 'json',
        success: function(data) {
            console.log(data)
            if (data.status === 200 && data.data) {
                window.location.href = '/question/detail/' + data.data.qid + encodeURI('?m=创建成功&e=success')
            } else if (data.status === 200001 || data.status === 200002) {
                $('#editorForm').prepend("<div id='regMessage' class='alert alert-danger'>" + data.message + "</div>")
            }
        }
    })
    return false
})
