let cur_button = "nothing"

$('#refresh_image').click(function(){

    cur_button = 'refresh_image'
    
    $.get('/update_image/', function(data){
        $('#big_image').attr("src", data)
    });

});

$('#calculate').click(function(){

    cur_button = 'calculate'

    $('#refresh_image').attr("class", "btn-large disabled styled")
    $('#calculate').attr("class", "btn-large disabled styled")
    $('#download_image').attr("class", "btn-large disabled styled")
    $('#download_keypoints').attr("class", "btn-large disabled styled")    

    $.get('/calculate_keypoints/', function(data){
        $('#big_image').attr("src", data)
    });


});

$('#download_image').click(function(){
    cur_button = 'download_image'
});    

$('#download_keypoints').click(function(){
    cur_button = 'download_keypoints'
});

$(document).on("ajaxSend", function() {

    $("#preloader").css('visibility', 'visible')

}).on("ajaxStop", function(){

    $("#preloader").css('visibility', 'hidden')

    if (cur_button === 'refresh_image') {
        $('#refresh_image').attr("class", "waves-effect btn-large styled")
        $('#calculate').attr("class", "waves-effect btn-large styled")
        $('#download_image').attr("class", "btn-large disabled styled")
        $('#download_keypoints').attr("class", "btn-large disabled styled")
    }
    else {
        if (cur_button === 'calculate') {
            $('#refresh_image').attr("class", "waves-effect btn-large styled")
            $('#calculate').attr("class", "waves-effect btn-large styled")
            $('#download_image').attr("class", "waves-effect btn-large styled")
            $('#download_keypoints').attr("class", "waves-effect btn-large styled")
        }
    }

});

