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
    let contactList = document.getElementById('contact-table');
    let template = JsT.loadById('template-contact-row');

    contactList.innerHTML += template.render({
        name: name,
        phone: phone
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
                citizenName: 'hanne',
                username: 'hanne123',
                email: 'hanne@blah.com',
                address: 'ølborgvej 13',
                city: 'ølborg',
                postalCode: '9220'
            });
        },
        error: function (response){
            console.log('no citizen found');

            let infoBox= document.getElementById('citizen-info');
            let template = JsT.loadById('template-citizen-info');

            infoBox.innerHTML = template.render({
                citizenName: 'hanne',
                username: 'hanne123',
                email: 'hanne@blah.com',
                address: 'ølborgvej 13',
                city: 'ølborg',
                postalCode: '9220'
            });
        }
    });

}
