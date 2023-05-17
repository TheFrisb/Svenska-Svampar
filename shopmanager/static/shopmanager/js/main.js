$(document).ready(function(){
    let token = $('input[name="csrfmiddlewaretoken"]').val();

    $(document).on('click', '.dismiss-userBtn', function(){
        let button = $(this);
        let applicant_id = parseInt(button.data('registrant-id'));

        $.ajax({
            url: 'dismiss-applicant/',
            type: 'POST',
            data: {
                'applicant_id': applicant_id,
                csrfmiddlewaretoken: token,
            },
            success: function(response){
                $(button).closest(".applicationHolder").remove();
            }
        });
    });
});