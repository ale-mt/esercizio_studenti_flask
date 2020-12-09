$(document).ready(function() {

    $('.updateButton').on('click', function() {

        var member_id = $(this).attr('student_id');

        req = $.ajax({
            url : '/update',
            type : 'POST',
            data : { id : member_id }
        });

        req.done(function(data) {

            $('.memberSection'+member_id).fadeOut(1000);

        });
    });

});
