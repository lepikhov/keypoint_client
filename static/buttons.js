$('#refresh_image').click(function(){
    $.get('/update_image/', function(data){
        $('#big_image').attr("src", data)
    });

    $('#refresh_image').attr("class", "waves-effect btn-large styled")
    $('#calculate').attr("class", "waves-effect btn-large styled")
    $('#download_image').attr("class", "btn-large disabled styled")
    $('#download_keypoints').attr("class", "btn-large disabled styled")
});

$('#calculate').click(function(){
    $.get('/calculate_keypoints/', function(data){
        $('#big_image').attr("src", data)
    });

    $('#download_image').attr("class", "waves-effect btn-large styled")
    $('#download_keypoints').attr("class", "waves-effect btn-large styled")
});

$('#download_image').click(function(){
    console.log('download_image click')
});    

$('#download_keypoints').click(function(){
    console.log('download_keypoints click')
});

