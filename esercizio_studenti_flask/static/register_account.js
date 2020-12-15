$(document).ready(function() {

    // crea elemento form e ogni input da inserirci
    var form = document.createElement("form");
    form.className = "mt-4 mb-4"

    var Email = document.createElement("input");
    Email.className = "form-control form-control-lg my-1"
    Email.setAttribute("type", "email");
    Email.setAttribute("name", "email");
    Email.setAttribute("placeholder", "your@email.com");


    var Password = document.createElement("input");
    Password.className = "form-control form-control-lg my-1"
    Password.setAttribute("type", "password");
    Password.setAttribute("name", "password");
    Password.setAttribute("placeholder", "secretpassword");


    var ConfirmPassword = document.createElement("input");
    ConfirmPassword.className = "form-control form-control-lg my-1"
    ConfirmPassword.setAttribute("type", "password");
    ConfirmPassword.setAttribute("name", "confirm_password");
    ConfirmPassword.setAttribute("placeholder", "retypesecretpassword");

    var div_admin = document.createElement("div");
    var div_moderatore = document.createElement("div");

    //  checkbox per admin e moderatore
    var Admin = document.createElement("input");
    Admin.setAttribute("type", "checkbox");
    Admin.setAttribute("name", "ruolo");
    Admin.id="admin";
    Admin.value="admin";

    var AdminLabel = document.createElement("Label");
    AdminLabel.setAttribute("for", "admin");
    AdminLabel.innerHTML = "Admin ";

    div_admin.appendChild(AdminLabel);
    div_admin.appendChild(Admin);


    var Moderatore = document.createElement("input");
    Moderatore.setAttribute("type", "checkbox");
    Moderatore.setAttribute("name", "ruolo");
    Moderatore.value="moderatore";
    Moderatore.id = "moderatore";

    var ModeratoreLabel = document.createElement("Label");
    ModeratoreLabel.setAttribute("for", "moderatore");
    ModeratoreLabel.innerHTML = "Moderatore ";

    div_moderatore.appendChild(ModeratoreLabel)
    div_moderatore.appendChild(Moderatore)


    // bottone di submit edit e delete
    var s = document.createElement("input");
    s.className = "btn btn-primary";
    s.setAttribute("type", "button");
    s.setAttribute("value", "Submit");
    s.setAttribute("name", "submit");

    var e = document.createElement("input");
    e.className = "btn btn-info mr-1"
    e.setAttribute("type", "button");
    e.setAttribute("value", "Edit");
    e.setAttribute("name", "edit");
    e.hidden = true;

    var d = document.createElement("input");
    d.className = "btn btn-danger"
    d.setAttribute("type", "button");
    d.setAttribute("value", "Delete");
    d.setAttribute("name", "delete");
    d.hidden = true;


    var PasswordLabel = document.createElement("Label");
    PasswordLabel.setAttribute("for", "password");
    PasswordLabel.innerHTML = "Password: ";

    var confirm_password_label = document.createElement("Label");
    confirm_password_label.setAttribute("for", "confirm_password");
    confirm_password_label.innerHTML = "Conferma Password: ";

    var EmailLabel = document.createElement("Label");
    EmailLabel.setAttribute("for", "email");
    EmailLabel.innerHTML = "Email: ";

    // div di invalid-feedback per ogni <input>
    var Invalid_feedback_email = document.createElement('div')
    Invalid_feedback_email.className = "invalid-feedback email"
    Invalid_feedback_email.innerHTML = ""

    var Invalid_feedback_password = document.createElement('div')
    Invalid_feedback_password.className = "invalid-feedback password"
    Invalid_feedback_password.innerHTML = ""

    var Invalid_feedback_confirm_password = document.createElement('div')
    Invalid_feedback_confirm_password.className = "invalid-feedback confirm_password"
    Invalid_feedback_confirm_password.innerHTML = ""


 // prendi parametro id da url ?id=x
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    id = null

    if(urlParams.has('id')){
        id = urlParams.get('id')
        console.log("id utente: " + id);

        $.getJSON( "/register/user/getdata/" + id, function( data ) {
            console.log(data.user)

            $("input").hide();
            $("label").hide();

            $("label[for='email'").show();
            $("label[for='admin'").show();
            $("label[for='moderatore'").show();
            $("input[type='button'").show();
            $("input[type='checkbox'").show();
            $("input[name='email'").show();

            $.each( data.user, function( key, val ) { // popolo ogni input tag con il suo valore corrispondente
                $("input[name='" + key + "']").val(val); // input[name=email]...
                console.log(key, val);
            });
        });

        // se ha ricevuto id nascondi bottone di submit perche non sto facendo un inserimento
        s.hidden = true;
        e.hidden = false;
        d.hidden = false;


    }


    form.append(EmailLabel);
    form.append(Email);
    form.append(Invalid_feedback_email);

    form.append(PasswordLabel);
    form.append(Password);
    form.append(Invalid_feedback_password);

    form.append(confirm_password_label);
    form.append(ConfirmPassword);
    form.append(Invalid_feedback_confirm_password);

    form.appendChild(div_admin);
    form.appendChild(div_moderatore);

    form.append(s);
    form.append(e);
    form.append(d);

    document.getElementById("container-form").appendChild(form);

    function formValidation(data) {

    $('input.is-invalid').each(function(){
        $(this).removeClass('is-invalid'); // rimuove is-invalid dagli <input>
    });

    $('div.invalid-feedback').each(function(){
        $(this).removeClass('d-block'); // nasconde i <div class="invalid-feedback">
        $(this).addClass('d-none');
    });

    if (Array.isArray(data.target)) { // se viene restituito un array di errori cicla dentro di essi e gestisci la form

        console.log("==== target errori: ====")
        data.target.forEach(function(item) {
            console.log(item)
            $("input[name='"+item+"']").addClass('is-invalid');
            $('div.invalid-feedback.'+item).html(data.error);
            $('div.invalid-feedback.'+item).addClass('d-block');
        });
        console.log("=============")

        } else {    // viene restituito un array anche per 1 solo errore, assenza di array = nessun errore
            console.log('No errors')
            if (data.redirect) {
                window.location.href = data.redirect;
            }
        }
    }

    $(e).click(function(){
        console.log('premuto edit');
        req = $.ajax ({
            url: '/register/admin',
            type: 'POST',
             data: JSON.stringify({email:Email.value, admin:Admin.checked, moderatore:Moderatore.checked, id:id, action: "edit"}),
            dataType: "json",
            contentType: "application/json; charset=utf-8"
        });

        req.done(function(data) {
            console.log("richiesta conclusa")

            formValidation(data);

            console.log('form target: ' + data.target);
            console.log('error log: ' + data.error)


        });
    });

    $(d).click(function(){
        console.log('premuto delete');

        req = $.ajax ({
            url: '/register/admin',
            type: 'POST',
            data: JSON.stringify({email: Email.value, action: "delete"}),
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
        console.log("submit");
        req = $.ajax ({
            url: '/register/admin',
            type: "POST",
            data: JSON.stringify({email:Email.value, password: Password.value, confirm_password: ConfirmPassword.value,
             admin:Admin.checked, moderatore:Moderatore.checked, action: "submit"}),
            dataType: "json",
            contentType: "application/json; charset=utf-8"
        });

        // a richiesta conclusa rimuovi tutti i precedenti errori di validazione e nel caso rimettili dove opportuno
        req.done(function(data) {
            console.log("richiesta conclusa");

            console.log(data)
            formValidation(data);

            console.log('form target: ' + data.target);
            console.log('error log: ' + data.error)
        });

    });

})
