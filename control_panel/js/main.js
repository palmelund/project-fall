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

function GetContactList () {
    let box = document.getElementById('contact-list');
}

function AddNewContact (name, phone) {
    $.ajax({
        url: 'addcontact/tolis',
        type: 'POST',
        data: {phone: phone},
        success: function (response) {
            renderContactList();

        },
        error: function (response) {
            console.log("addNewContact: " + response);
            renderContactList();
        }
    });
}


function RenderContactList () {
    let contactList = document.getElementById('contact-table');
    let template = JsT.loadById('template-contact-row');
    let clst;

    $.ajax({
        url: 'getcontact/list',
        type: 'GET',
        success: function (response) {
            clst = response;
        },
        error: function (response) {
            console.log("renderContactList: " + response);
        }
    });

    clst = [{name: "Anne Jensen", phone: "12345678"}, {name: "Paul Jensen", phone: "87654321"}];

    for (i = 0; i < clst.length; i++){
        contactList.innerHTML += template.render({
            name: clst[i].name,
            phone: clst[i].phone
        });
    }
}

function RemoveContact (phone) {
    $.ajax({
        url: 'removecontact/tolis',
        type: 'POST',
        data: {phone: phone},
        success: function (response) {
            renderContactList(response);
        },
        error: function (response) {
            console.log("removeContact: " + response);
        }
    });

}

function SearchForCitizen (phone) {
    let searchNr = document.getElementById("").value;

    $.ajax({
        url: 'search/url',
        type: 'GET',
        data: {data: phone},
        success: function (response){
            let tableOut = document.getElementById('search-result');
            let template = JsT.loadById('template-search-result-row');

            response.foreach(function (name, phoneNr) {
                tableOut.innerHTML += template.render({
                    name: name,
                    phone: phoneNr
                });
            });

        },
        error: function (response){
            console.log('no citizen found');
        }
    });
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
                citizenName: 'Fru Jensen',
                email: 'jensen@hotmail.com',

                address: 'Aalborgvej 13',
                city: 'Aalborg',
                postalCode: '9220'
            });
        },
        error: function (response){
            console.log('no citizen found');

            let infoBox = document.getElementById('citizen-info');
            let template = JsT.loadById('template-citizen-info');
            infoBox.className += " box";

            infoBox.innerHTML = template.render({
                citizenName: 'Fru Jensen',
                email: 'jensen@hotmail.com',
                address: 'Aalborgvej 13',
                city: 'Aalborg',
                postalCode: '9220'
            });
        }
    });
}
