$("#button").click(function (e) {
    let num1 = $('#num1').val();
    let num2 = $('#num2').val();
    $.ajax({
        url: '/divide?num1=' + num1 + '&num2=' + num2,
        method: 'get',
        success: function (data) {
            $('#result2').html('200 ' + data['result'])
        },
        error: function (error) {
            $('#result2').html(error.status + error.statusText)
        }
    })
});

$("#login").click(function (e) {
    let username = $('#username').val();
    let password = $('#password').val();
    $.ajax({
        url: '/login',
        method: 'post',
        contentType: 'application/json',
        data: JSON.stringify({
            name: username,
            password: password
        }),
        success: function (data) {
            $('#result2').html('200 ' + data['result'])
        },
        error: function (error) {
            $('#result1').html(error.status + error.statusText)
        }
    })
});