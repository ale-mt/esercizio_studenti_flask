$(document).ready(function() {
    console.log(errore)

    // Create a form dynamically
    var form = document.createElement("form");
    form.className = "mt-4 mb-4"

    var selectList = document.createElement("select");
    selectList.id = "mySelect";
    selectList.className = "form-control form-control-lg my-1 check_students"
    selectList.setAttribute("name", "id");
    selectList.hidden = true;

    var Name = document.createElement("input");
    Name.className = "form-control form-control-lg my-1"
    Name.setAttribute("type", "text");
    Name.setAttribute("name", "name");
    Name.setAttribute("placeholder", "Nome");
    Name.required = true;

    var Lastname = document.createElement("input");
    Lastname.className = "form-control form-control-lg my-1"
    Lastname.setAttribute("type", "text");
    Lastname.setAttribute("name", "lastname");
    Lastname.setAttribute("placeholder", "Cognome");
    Lastname.required = true;

    var Email = document.createElement("input");
    Email.className = "form-control form-control-lg my-1"
    Email.setAttribute("type", "email");
    Email.setAttribute("name", "email");
    Email.setAttribute("placeholder", "email@email.email");
    Email.required = true;


    var Invalid_feedback_name = document.createElement('div')
    Invalid_feedback_name.className = "invalid-feedback name"
    Invalid_feedback_name.innerHTML = ""

    var Invalid_feedback_lastname = document.createElement('div')
    Invalid_feedback_lastname.className = "invalid-feedback lastname"
    Invalid_feedback_lastname.innerHTML = ""

    var Invalid_feedback_age = document.createElement('div')
    Invalid_feedback_age.className = "invalid-feedback age"
    Invalid_feedback_age.innerHTML = ""

    var Invalid_feedback_email = document.createElement('div')
    Invalid_feedback_email.className = "invalid-feedback email"
    Invalid_feedback_email.innerHTML = ""

    var Age = document.createElement("input");
    Age.className = "form-control form-control-lg my-1"
    Age.setAttribute("type", "number");
    Age.setAttribute("name", "age");
    Age.setAttribute("placeholder", "18");
    Age.required = true;

    // Create a submit button
    var s = document.createElement("input");
    s.className = "btn btn-primary";
    s.setAttribute("value", "Submit");
    s.setAttribute("name", "submit");

    // Create an edit button
    var e = document.createElement("input");
    e.className = "btn btn-info mr-1"
    e.setAttribute("type", "button");
    e.setAttribute("value", "Edit");
    e.setAttribute("name", "edit");
    e.hidden = true;

    // Create a delete button
    var d = document.createElement("input");
    d.className = "btn btn-danger"
    d.setAttribute("type", "button");
    d.setAttribute("value", "Delete");
    d.hidden = true;


    // get id from url
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    id = null

    if(urlParams.has('id')){
        id = urlParams.get('id')
        console.log(id);

        selectList.hidden = false;

        $.getJSON( "/register/getdata/" + id, function( data ) {
            console.log(data.lista_id);
            console.log(data.studente)

            //Create and append the options
            for (var i = 0; i < data.lista_id.length; i++) {
            var option = document.createElement("option");
                option.value = data.lista_id[i];
                option.text = "Studente con ID: " + data.lista_id[i];
                option.className = "check_students";
                selectList.appendChild(option);
            }

            $.each( data.studente, function( key, val ) {
                $("input[name='" + key + "']").val(val)
                console.log(key, val);
            });
            $("select[name='id']").val(data.studente.id)
        });


        s.hidden = true;
        e.hidden = false;
        d.hidden = false;

    }

    form.append(selectList);
    form.append(Name);
    form.append(Invalid_feedback_name);
    form.append(Lastname);
    form.append(Invalid_feedback_lastname);
    form.append(Age);
    form.append(Invalid_feedback_age);
    form.append(Email);
    form.append(Invalid_feedback_email);
    form.append(s);
    form.append(e);
    form.append(d);

    document.getElementById("container-form").appendChild(form);

    $(e).click(function(){
        console.log('premuto edit');
        req = $.ajax ({
            url: '/register/student',
            type: 'POST',
            data: JSON.stringify({id: selectList.value, name:Name.value, lastname: Lastname.value, age: Age.value, email:Email.value, action: "edit"}),
            dataType: "json",
            contentType: "application/json; charset=utf-8"
        });

        req.done(function(data){
            console.log("richiesta conclusa")

            console.log('form target: ' + data.target);
            console.log('error log: ' + data.error)

            $('input.is-invalid').each(function(){
                $(this).removeClass('is-invalid'); // rimuove is-invalid dagli <input>
            });

            $('div.invalid-feedback').each(function(){
                $(this).removeClass('d-block'); // nasconde i <div class="invalid-feedback">
                $(this).addClass('d-none');
            });

            if (Array.isArray(data.target)) { // se viene restituito un array di errori cicla dentro di essi e gestisci la form

                data.target.forEach(function(item) {
                    console.log(item)
                    $("input[name='"+item+"']").addClass('is-invalid');
                    $('div.invalid-feedback.'+item).html(data.error);
                    $('div.invalid-feedback.'+item).addClass('d-block');
                });

            } else {    // viene restituito un array anche per 1 solo errore, assenza di array = nessun errore
                console.log('No errors')
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            }
        });
    });

    $(d).click(function(){
        console.log('premuto delete');

        req = $.ajax ({
            url: '/register/student',
            type: 'POST',
            data: JSON.stringify({id: selectList.value, name:Name.value, lastname: Lastname.value, age: Age.value, email:Email.value, action: "delete"}),
            dataType: "json",
            contentType: "application/json; charset=utf-8"
        });

        req.done(function(data){
            if(data.redirect){
                window.location.href = data.redirect;
            }
        });
    });

    $(s).click(function(){  // bottone s di submit premuto
            req = $.ajax ({
            url: '/register/student',
            type: "POST",
            data: JSON.stringify({name:Name.value, lastname: Lastname.value, age: Age.value, email:Email.value, action: "submit"}),
            dataType: "json",
            contentType: "application/json; charset=utf-8"
        });

        // a richiesta conclusa rimuovi tutti i precedenti errori di validazione e nel caso rimettili dove opportuno
        req.done(function(data) {
            console.log("richiesta conclusa");
            console.log('form target: ' + data.target);
            console.log('error log: ' + data.error)

            $('input.is-invalid').each(function(){
                $(this).removeClass('is-invalid'); // rimuove is-invalid dagli <input>
            });

            $('div.invalid-feedback').each(function(){
                $(this).removeClass('d-block'); // nasconde i <div class="invalid-feedback">
                $(this).addClass('d-none');
            });

            if (Array.isArray(data.target)) { // se viene restituito un array di errori cicla dentro di essi e gestisci la form

                data.target.forEach(function(item) {
                    console.log(item)
                    $("input[name='"+item+"']").addClass('is-invalid');
                    $('div.invalid-feedback.'+item).html(data.error);
                    $('div.invalid-feedback.'+item).addClass('d-block');
                });

            } else {    // viene restituito un array anche per 1 solo errore, assenza di array = nessun errore
                console.log('No errors')
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            }

        });

    });

    $('.check_students').change(function() {
        var student_id = $(this).val();
        req = $.ajax({
            url : '/register/update_insert',
            type : 'POST',
            data : { id : student_id }
        });

        req.done(function(data) {
            $.each(data, function(key, val) {
                $("input[name='"+key+"']").val(val)
            });
        });
    });
    });
