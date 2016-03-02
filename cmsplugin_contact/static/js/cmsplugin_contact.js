(function($){
    "use strict";
    $(function(){
    
        $('#cmsplugin-contact-form').submit(function(evt){
            var $form = $(this);
            evt.preventDefault();

            function handleResponse(data){
                console.log(data);
                if (data.ok) { // Success!
                    $('#confirmation-message').fadeIn();
                    $form.hide();
                }
            
                else {
                    //If recaptcha ( needs fixing! )
                    //Recaptcha.reload();
                    $('span.error_msg').remove();
                    $.each(data, function(key, value){
                       $('div.input-group.' + key).append('<span class="error_msg">' + value + '</span>');
                    });
                }
            }
    
            $.ajax({
                type: 'POST',
                url: $form.attr('action'),
                beforeSend: function() {
                    $('div.form-overlay').fadeIn();
                },
                complete: function() {
                    $('div.form-overlay').fadeOut();
                },
                data: $form.serialize()
            }).always(handleResponse);
        });
    
    });
}(window.jQuery));