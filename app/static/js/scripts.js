
(function($){
    function slugify(Text)
    {
        return Text
            .toLowerCase()
            .replace(/[^\w ]+/g,'')
            .replace(/ +/g,'-');
    }

    // Slugify the edit_post templates slug field on the fly
    $("#title-form").keyup(function() {
        $('#slug-form').val(slugify($(this).val()));
    });

    function flash(msg, category) {
        html = "<div class='alert alert-dismissable " + category + "'>\
                <button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>\
                " + msg + "\
                </div>"

        $('#flash-msg').html(html);
    }

    // enable bootstrap's file inputs
    $('input[type=file]').bootstrapFileInput();

    $('.remove-post').click(function() {
        var par = $(this).parent()
        var id = par.attr('id');
        $.ajax({
            url: '',
            type: 'POST',
            data: {
                'slug' : id,
                'type' : 'DELETE_POST',
            },

            success: function (result) {
                if (result != 'error') {
                    par.parent().hide()
                };
            }
        });
    });

    $('.remove-user').click(function() {
        var par = $(this).parent()
        var id = par.attr('id');
        $.ajax({
            url: '',
            type: 'POST',
            data: {
                'id' : id,
                'type' : 'DELETE_USER',
            },

            success: function (result) {
                // TODO: perhaps handle the error a better way?
                if (result != 'error') {
                    par.parent().hide()
                }
                else {
                    flash("An admin user can not be deleted.", "alert-warning");
                };
            }
        });
    });



})(window.jQuery);
