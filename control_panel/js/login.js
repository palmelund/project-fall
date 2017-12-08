window.onload = RenderLoginView();

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
