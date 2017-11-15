function getNewCitizenData(){
    var obj = new Object();

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
        url: "/fisk/fisk",
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

// contactTable = document.getElementById('citizen-info-contact-table');
// contactTable.style.height = document.getElementById('citizen-info').clientHeight;