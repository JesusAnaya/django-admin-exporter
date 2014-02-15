
(function($){
    $(document).on('ready', function(){

        $('#export-form').on('submit', function(){
            var parameters = "";
            var counter = 0;
            $('input[type="checkbox"]:checked').each(function(){
                if (counter === 0) {
                    parameters = $(this).attr('name');
                } else {
                    parameters += ',' + $(this).attr('name');
                }
                counter ++;
            });
            $("#export-data").val(parameters);
        });
    });
})
((jQuery));
