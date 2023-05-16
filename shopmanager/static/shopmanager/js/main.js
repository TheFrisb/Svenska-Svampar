$(document).ready(function(){
    let token = $('input[name="csrfmiddlewaretoken"]').val();
    $(document).on('click', '#export', function(){
        let date_from = $('#date_from').val();
        let date_to = $('#date_to').val();
        let option = $('#option').val();
        $.ajax({
            url: 'export-orders-as-pdf/',
            type: 'GET',
            data: {
                'date_from': date_from,
                'date_to': date_to,
                'option': option,
                csrfmiddlewaretoken: token,
            },
            success: function(response){
                var blob = new Blob([response]);
                var url = window.URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = 'orders.pdf';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            },
            error: function(xhr, textStatus, errorThrown) {
                // Process the error response
                $("#response").html(xhr.responseText);
              }
        });
    });
});