$("#button").click(function (e) {
    let num1 = $('#num1').val();
    let num2 = $('#num2').val();
    $.ajax({
        url: '/divide?num1=' + num1 + '&num2=' + num2,
        method: 'get',
        success: function (data) {
            console.log(data)
        },
        error: function (error) {
            console.log(error)
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
            console.log(data)
        },
        error: function (error) {
            console.log(error)
        }
    })
});