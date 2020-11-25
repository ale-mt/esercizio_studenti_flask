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


    $('.check_students').change(function() {

        var student_id = $(this).val();
        console.log(student_id)
        req = $.ajax({
            url : '/update_insert',
            type : 'POST',
            data : { id : student_id }
        });

        req.done(function(data) {
            console.log(data)
            $("input[name='email']").val(data['email'])
            $("input[name='name']").val(data['name'])
            $("input[name='lastname']").val(data['lastname'])
            $("input[name='age']").val(data['age'])
        });
    });
});
