
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

    // enable bootstrap's file inputs
    $('input[type=file]').bootstrapFileInput();

    $('.remove-post').click(function() {
        var id = $(this).parent().attr('id');
        $.ajax({
            url: '',
            type: 'POST',
            data: {
                'slug' : id,
                'type' : 'DELETE_POST',
            },

            success: function (result) {
                console.log("deleted post " + id);
            }
        });
    });

    $('.remove-user').click(function() {
        var id = $(this).parent().attr('id');
        $.ajax({
            url: '',
            type: 'POST',
            data: {
                'id' : id,
                'type' : 'DELETE_USER',
            },

            success: function (result) {
                console.log("deleted user " + id);
            }
        });
    });
})(window.jQuery);
