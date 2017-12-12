// Global variables
let user = new Object();
let container = document.getElementById('container');
let contactlst = [];

toastr.options = {
    "positionClass" : "toast-bottom-right",
    "showDuration": "300"
};

window.onload = RenderLoginView();

function GetContactList() {
    $.ajax({
        url: 'https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/contact',
        type: 'GET',
        success: function(response) {
            let fixedResponse = response.body.substring(1, response.body.length - 1);
            let json = JSON.parse(fixedResponse);

            for (let i = 0; i < json.length; i++) {
                contactlst[i] = json[i];
            }
        },
        error: function(response) {
            console.log("Couldn't fetch contactlist");
        }
    });
}

function AddNewCitizen(){
    let form = $("#citizen-form");

    $.ajax({
        url: '/fisk/fisk',
        type: 'POST',
        data: form.serialize(),
        success: function(respose) {
            console.log("success");
        },
        error: function(response) {
            console.log("error");
        }
    });
    form[0].reset();
}

function AddNewContact (id, name) {
    let table = document.getElementById('contact-table');
    let template = JsT.loadById('template-contact-row');

    table.innerHTML += template.render({
        name: name,
        id: id
    });

    contactlst.find(function (contact) {
        if (contact.id == id){
            user.body.contacts[user.body.contacts.length] = contact;
        }
    });
}


function RenderContactList () {
    let contactList = document.getElementById('contact-table');
    let template = JsT.loadById('template-contact-row');

    contactList.innerHTML = "";
    for (i = 0; i < user.body.contacts.length; i++){
        contactList.innerHTML += template.render({
            name: user.body.contacts[i].name,
            id: user.body[i].id
        });
    }
}

function RemoveContact (phone) {
}

function SearchForContact(event) {
    if (event.key !== "Enter") { return; }

    let query = document.getElementById('search-contact-box').value;
    let tableOut = document.getElementById('search-result');
    let template = JsT.loadById('template-search-result-row');
    let result = [];

    for (let i = 0, count = 0; i < contactlst.length; i++) {
        let exists = false;
        match = (contactlst[i].email).includes(query);

        user.body.contacts.find(function (contacts) {
            if (contacts.id == contactlst[i].id){
                exists = true;
            }
        });
        if (match && !exists){
            result[count] = contactlst[i];
            count++;
        }
    }

    tableOut.innerText = "";
    for (let i = 0; i < result.length; i++) {
        tableOut.innerHTML += template.render({
            name: result[i].name,
            id: result[i].id
        });
    }
}

function RenderCitizenInfo (phone) {
    // let infoBox = document.getElementById('citizen-info');
    // let template = JsT.loadById('template-citizen-info');

    $.ajax({
        url: 'get/url',
        type: 'GET',
        data: {data: phone},
        success: function (response){
            let infoBox = document.getElementById('citizen-info');
            let template = JsT.loadById('template-citizen-info');
            infoBox.className += " box";

            infoBox.innerHTML = template.render({
                citizenName: user.body.name,
                email: user.body.email,
                address: user.body.address,
                city: user.body.city,
                postalCode: user.body.postnr
            });
        },
        error: function (response){
            console.log('no citizen found');

            let infoBox = document.getElementById('citizen-info');
            let template = JsT.loadById('template-citizen-info');
            infoBox.className += " box";

            infoBox.innerHTML = template.render({
                citizenName: user.body.name,
                email: user.body.email,
                address: user.body.address,
                city: user.body.city,
                postalCode: user.body.postnr
            });
        }
    });
    RenderContactList();
}

// login
function RenderLoginView() {
    let template = JsT.loadById('template-login');

    container.classList.add('container');
    container.innerHTML = template.render();
}

function RenderRegisterView() {
    let template = JsT.loadById('template-register');

    container.innerHTML = template.render();
}

function RenderRegisterCitizenView() {
    let view = document.getElementById('register-user-view');
    let template = JsT.loadById('template-register-citizen');
    view.innerHTML = template.render();
}

function RenderRegisterContactView() {
    let view = document.getElementById('register-user-view');
    let template = JsT.loadById('template-register-contact');
    view.innerHTML = template.render();
}

function Login () {
    let form = $('form').serialize();

    $.ajax({
        url: 'https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user',
        type: 'GET',
        data: form,
        success: function (response) {
            user = JSON.parse(JSON.stringify(response));
            user.body = (JSON.parse(user.body));

            if (user.statusCode == 200 && user.body.role == "citizen") {
                let container = document.getElementById('container');
                let template = JsT.loadById('template-citizen-view');

                container.classList.add('wrapper');
                container.classList.remove('container');
                container.innerHTML = template.render();
                GetContactList();
            }
            else if (user.statusCode == 400 && user.body.role == "citizen") {
                toastr.error("Forkerte login oplysninger");
            }
            else if (user.statusCode == 200 && user.body.role == "contact") {
                toastr.error("Bruger er ikke en borger");
            }
            else {
                toastr.error("Login mislykkes");
            }
        },
        error: function (response) {
            console.log("Login attempt failed");
        }
    });
}

function RegisterNewUser(role) {
    let pass1 = $('#add-new-user-form').find('input[name=password]').val();
    let pass2 = $('#add-new-user-form').find('input[name=passwordConfirm]').val();

    if (pass1 != pass2) {
        toastr.error("Kodeord er ikke ens");
        return;
    }

    let userData= "";
    let name = $('#add-new-user-form').find('input[name=name]').val();
    let email = $('#add-new-user-form').find('input[name=email]').val();
    let password = $('#add-new-user-form').find('input[name=password]').val();

    if (role == "contact") {
        userData = "{'id': '-1', " + "'name': '" + name + "', 'email': '" + email +
            "', 'role': 'contact', 'devices': []}";
    }
    else {
        let add = $('#add-new-user-form').find('input[name=address]').val();
        let city = $('#add-new-user-form').find('input[name=city]').val();
        let zip = $('#add-new-user-form').find('input[name=postcode]').val();
        userData = "{'id': '-1', " + "'name': '" + name + "', 'email': '" + email +
            "', 'role': 'citizen', 'address': '" + add + "', 'city': '" + city + "', 'postnr': '"+ zip + "', 'devices': [], 'contacts': []}";
    }

    $.ajax({
    url: 'https://prbw36cvje.execute-api.us-east-1.amazonaws.com/dev/user',
    type: 'POST',
        data: userData,
        headers: {'user': userData, 'password': password.toString()},
        contentType: 'application/json',
        success: function (response) {
            RenderLoginView();
            toastr.success("Ny bruger blev tilføjet");
        },
        error: function (response) {
            toastr.error("Ny bruger kunne ikke tilføjet");
        }
    });
}
