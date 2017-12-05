function getNewCitizenData(){
    let obj = new Object();

    obj.name = $('#name').val();
    obj.email = $('#email').val();
    obj.username = $('#username').val();
    obj.address = $('#address').val();
    obj.city = $('#city').val();
    obj.post = $('#post-code').val();

    $("#citizen-form")[0].reset();
    return JSON.stringify(obj);
}

function addNewCitizen(){
    $.ajax({
        url: '/fisk/fisk',
        type: 'POST',
        data: {data: getNewCitizenData()},
        success: function(respose){
            console.log("success");
        },
        error: function(response){
            console.log("error");
        }
    });
}

function getContactList () {
    let box = document.getElementById('contact-list');
}

function addNewContact (name, phone) {
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


function renderContactList () {
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

function removeContact (phone) {
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

function searchForCitizen (phone) {
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

function renderCitizenInfo (phone) {
    // let infoBox = document.getElementById('citizen-info');
    // let template = JsT.loadById('template-citizen-info');

    $.ajax({
        url: 'get/url',
        type: 'GET',
        data: {data: phone},
        success: function (response){
            let infoBox= document.getElementById('citizen-info');
            let template = JsT.loadById('template-citizen-info');

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

            let infoBox= document.getElementById('citizen-info');
            let template = JsT.loadById('template-citizen-info');

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


function login () {
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
