// Global variables
let baseURL = 'https://prbw36cvje.execute-api.us-east-1.amazonaws.com';
let user = new Object();
let container = document.getElementById('container');
let contactLst = [];
let citizenLst = [];
let currentCitizen;
let oldSearchQuery = "";
let deviceLst = [];

toastr.options = {
    "positionClass" : "toast-bottom-right",
    "showDuration": "300"
};

window.onload = RenderLoginView();


function GetContactList() {
    $.ajax({
        url: baseURL + '/dev/contact',
        type: 'GET',
        success: function(response) {
            if (response.statusCode !== "200") {
                console.log("Couldn't fetch contact list");
                toastr.error("Noget gik galt. Prøv at logge ind igen");
                return;
            }
            let json = JSON.parse(response.body);

            for (let i = 0; i < json.length; i++) {
                contactLst[i] = json[i];
            }
        },
        error: function(response) {
            console.log("Couldn't fetch contact list");
            console.log("Couldn't fetch contactlist");
        }
    });
}

function GetCitizenList() {
    $.ajax({
        url: baseURL + '/dev/citizen',
        type: 'GET',
        success: function(response) {
            if (response.statusCode !== "200") {
                console.log("Couldn't fetch citizen list");
                toastr.error("Noget gik galt. Prøv at logge ind igen");
                return;
            }

            let json = JSON.parse(response.body);
            for (let i = 0; i < json.length; i++) {
                citizenLst[i] = json[i];
            }

            RenderCitizenList();
        },
        error: function(response) {
            console.log("Couldn't fetch citizen list");
            toastr.error("Noget gik galt. Prøv at logge ind igen");
        }
    });
}

function AddNewContact (id, name) {
    let table = document.getElementById('contact-table');
    let template = JsT.loadById('template-contact-row');

    table.innerHTML += template.render({
        name: name,
        id: id
    });

    contactLst.find(function (contact) {
        if (contact.id == id){
            currentCitizen.contacts[currentCitizen.contacts.length] = contact;
        }
    });

    RenderSearchContact();
}

function RenderContactList () {
    let contactList = document.getElementById('contact-table');
    let template = JsT.loadById('template-contact-row');

    contactList.innerHTML = "";
    for (i = 0; i < currentCitizen.contacts.length; i++){
        contactList.innerHTML += template.render({
            name: currentCitizen.contacts[i].name,
            id: currentCitizen.contacts[i].id
        });
    }
    console.log(contactLst);
}

function RemoveContact (id) {
    let index;
    for (let i = 0; i < currentCitizen.contacts.length; i++) {
        if (currentCitizen.contacts[i].id == id) {
            index = i;
            break;
        }
    }

    currentCitizen.contacts.splice(index, 1);
    RenderContactList();
    RenderSearchContact();
}

function RenderSearchContact(oldQuery = null) {
    let tableOut = document.getElementById('search-result');
    let template = JsT.loadById('template-search-result-row');
    let result = [];

    let query = oldQuery == null ?
        document.getElementById('search-contact-box').value :
        oldQuery;

    for (let i = 0, count = 0; i < contactLst.length; i++) {
        let exists = false;
        match = (contactLst[i].email).includes(query);

        currentCitizen.contacts.find(function (contacts) {
            if (contacts.id == contactLst[i].id) {
                exists = true;
            }
        });

        if (match && !exists) {
            result[count] = contactLst[i];
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

function SearchForContact(event) {
    if (event.key !== 'Enter') { return; }

    oldSearchQuery = null;
    RenderSearchContact();
}

function RenderCitizenList() {
    lst = document.getElementById('citizen-list');
    template = JsT.loadById('template-citizen-item');

    for (let i = 0; i < citizenLst.length; i++) {
        lst.innerHTML += template.render({
            name: citizenLst[i].name,
            id: citizenLst[i].id
        });
    }
}

function RenderCitizenInfo (id) {
    let infoBox = document.getElementById('citizen-info');
    let template = JsT.loadById('template-citizen-info');
    infoBox.className += " box";

    let citizen = citizenLst.find(function (citizen) {
        if (citizen.id == id) {
            return citizen;
        }
    });
    currentCitizen = citizen;
    deviceLst = currentCitizen.devices;

    infoBox.innerHTML = template.render({
        citizenName: citizen.name,
        email: citizen.email,
        address: citizen.address,
        city: citizen.city,
        postalCode: citizen.postnr
    });
    RenderContactList();
}

function UpdateCitizenToServer() {
    // console.log(currentCitizen);
    let id = currentCitizen.id;
    let name = currentCitizen.name;
    let email = currentCitizen.email;
    let add = currentCitizen.address;
    let city = currentCitizen.city;
    let zip = currentCitizen.postnr;
    let token = currentCitizen.token;
    let devices = JSON.stringify(deviceLst).replace(/\"/g, '\'');
    let contacts = JSON.stringify(currentCitizen.contacts).replace(/\"/g, '\'');


    userData = "{'id': '" + id + "', " + "'name': '" + name + "', 'email': '" + email +
        "', 'role': 'citizen', 'address': '" + add + "', 'city': '" + city +
        "', 'postnr': '"+ zip + "', 'devices': '" + devices + "', 'contacts': '" +
        contacts + "', 'token': '" + token + "}";


    // console.log(userData);

    $.ajax({
        url: baseURL + '/dev/user',
        contentType: 'application/json',
        headers: {'user': userData},
        type: 'PUT',
        success: function(response) {
            console.log("sucess");
            if (response.statusCode !== "200") {
                toastr.error(currentCitizen.name + " blev ikke gemt");
                return;
            }

            console.log(response);

            toastr.success(currentCitizen.name + "blev gemt");
        },
        error: function(response) {
            console.log(response);
            console.log("error");
            toastr.error(currentCitizen.name + " blev ikke gemt");
        }
    });
}

function RadioButton(device) {
    let alexa = document.getElementById('radio-alexa');
    let ifttt = document.getElementById('radio-ifttt');


    if (device === "alexa") {
        ifttt.removeAttribute('checked');
        alexa.setAttribute('checked', 'checked');
    }
    else {
        alexa.removeAttribute('checked');
        ifttt.setAttribute('checked', 'checked');
    }
}

function AddDevice() {
    let device = $('#add-device').find('input[name=device]:checked').val();
    let token = $('#add-device').find('input[name=token]').val();
    let obj = new Object();

    obj.devicetype = device;
    obj.token = token;
    obj.id = deviceLst.length;
    deviceLst[obj.id] = obj;

    RenderDeviceList();
}

function RemoveDevice(id) {
    let index;
    for (let i = 0; i < deviceLst.length; i++) {
        if (deviceLst[i].id == id) {
            index = i;
            break;
        }
    }

    deviceLst.splice(index, 1);
    RenderDeviceList();
}

function RenderDeviceList() {
    let table = document.getElementById('device-table');
    let template = JsT.loadById('template-device-row');

    table.innerHTML = "";
    for (let i = 0; i < deviceLst.length; i++) {
        table.innerHTML += template.render({
            devicetype: deviceLst[i].devicetype,
            id: deviceLst[i].id
        });
    }
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

function Login() {
    let form = $('form').serialize();

    $.ajax({
        url: baseURL + '/dev/user',
        type: 'GET',
        data: form,
        success: function (response) {
            user = JSON.parse(JSON.stringify(response));
            user.body = (JSON.parse(user.body));

            if (user.statusCode == 200 && user.body.role == 'citizen') {
                let container = document.getElementById('container');
                let template = JsT.loadById('template-citizen-view');

                container.classList.add('wrapper');
                container.classList.remove('container');
                container.innerHTML = template.render();

                console.log(user);

                GetContactList();
                GetCitizenList();
            }
            else if (user.statusCode == 400 && user.body.role == 'citizen') {
                toastr.error("Email eller kode passer ikke");
            }
            else if (user.statusCode == 200 && user.body.role == 'contact') {
                toastr.error("Bruger er ikke af typen borger");
            }
            else {
                toastr.error("Email eller kodeord passer ikke");
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

    let userData= '';
    let name = $('#add-new-user-form').find('input[name=name]').val();
    let email = $('#add-new-user-form').find('input[name=email]').val();
    let password = $('#add-new-user-form').find('input[name=password]').val();

    if (role == 'contact') {
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
    url: baseURL + '/dev/user',
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
