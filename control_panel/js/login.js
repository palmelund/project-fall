window.onload = RenderLoginView();

let user = new Object();

function RenderLoginView() {
    let container = document.getElementById('container');
    let template = JsT.loadById('template-login');

    container.innerHTML = template.render({});
}

function RenderRegisterView() {
    let container = document.getElementById('container');
    let template = JsT.loadById('template-register');

    container.innerHTML = template.render({});
}

function Login () {
    let form = $('form').serialize();

    $.ajax({
        url: 'https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user',
        type: 'GET',
        data: form,
        success: function (response) {
            user = JSON.parse(JSON.stringify(response));
            window.location.href = "citizenadmin.html";
        },
        error: function (response) {
            console.log("Login attempt failed");
        }
    });
}

function RegisterNewUser() {
    let form = $('#add-new-user-form').serialize();
    console.log(form);

    $.ajax({
        url: 'https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user',
        type: 'GET',
        data: form,
        success: function (response) {
            let res = (JSON.parse(response));
            console.log(res);
        },
        error: function (response) {
            console.log("ajax error");
        }
    });

    RenderLoginView();
}
