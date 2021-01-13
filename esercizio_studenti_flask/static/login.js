$(button).click(function(){  // bottone s di submit premuto
        console.log("submit");
        email = $(#emailinput).val()
        psw = $(#inputPassword).val()

        req = $.ajax ({
            url: '/login',
            type: "POST",
            data: JSON.stringify({email:email, password: psw}),
            dataType: "json",
            contentType: "application/json; charset=utf-8"
        });

        // a richiesta conclusa rimuovi tutti i precedenti errori di validazione e nel caso rimettili dove opportuno
        req.done(function(data) {
            console.log("richiesta conclusa");

            console.log(data)
            // formValidation(data);

            if (data.redirect) {
                window.location.href = data.redirect;
            }
        });

    });
