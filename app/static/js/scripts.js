
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

    $('.toggle-admin').click(function() {
        var ths = $(this)
        var id = $(this).parent().attr('id');

        var html = "&nbsp;<span class='glyphicon glyphicon-eye-open'></span>";

        $.ajax({
            url: '',
            type: 'POST',
            data: {
                'id' : id,
                'type' : 'TOGGLE_ADMIN',
            },

            success: function (result) {
                // TODO: perhaps handle the error a better way?
                if (result == '1') {
                    ths.removeClass('green glyphicon-eye-open').addClass('red glyphicon-eye-close');
                    ths.parent().next('.role-icon').addClass('glyphicon glyphicon-eye-open');
                }
                if (result == '0') {
                    ths.removeClass('red glyphicon-eye-close').addClass('green glyphicon-eye-open');
                    ths.parent().next('.role-icon').removeClass('glyphicon glyphicon-eye-open');
                }
                if (result == 'delete_self_error') {
                    flash("You can't remove your own admin status.", "alert-warning");
                }
            }
        });
    });

    $('.click-user').click(function(event) {
        var ths = $(this)
        var id = $(this).attr('id');
        event.preventDefault();

        $.ajax({
            url: '',
            type: 'POST',
            data: {
                'id' : id,
                'type' : 'GET_USER_DATA',
            },

            success: function (result) {
                $('#details-name').html(result["name"]);
                $('#details-role').html(result["role"]);
                $('#details-posts').html(result["posts"]);
            }
        });
    });



})(window.jQuery);
