let cur_button = "nothing"
let traits_is_predicted = false
let keypoints_is_calculated = false


$('#refresh_image').click(function(){

    cur_button = 'refresh_image'
    traits_is_predicted = false
    keypoints_is_calculated = false
    
    $.get('/update_image/', function(data){
        data = JSON.parse(data);
        if (data['media_type']==='video'){           
            if ($('#big_image').length) {
                $('#big_image').detach()
            }
            if ($('#video').length==0) {
                $('#media').append('<video id="video" preload="none" controls></video>')
            }    
            $('#video').attr("src", data['image_url'])
        }    
        else {
            if ($('#video').length) {
                $('#video').detach()
            }
            if ($('#big_image').length==0) {
                $('#media').append('<img id="big_image"/>')
            }    
            $('#big_image').attr("src", data['image_url'])
        }
    })

    if ($('#traits_table').length) $('#traits_table').detach()
    if ($('#traits_error_message').length) $('#traits_error_message').detach()        

})

$('#calculate').click(function(){

    cur_button = 'calculate'
    keypoints_is_calculated = true

    $('#refresh_image').attr("class", "btn-large disabled styled")
    $('#calculate').attr("class", "btn-large disabled styled")
    $('#download_image').attr("class", "btn-large disabled styled")
    $('#download_keypoints').attr("class", "btn-large disabled styled")    
    $('#predict_traits_any').attr("class", "btn-large disabled styled")
    $('#predict_traits_orlovskaya').attr("class", "btn-large disabled styled")    
    $('#download_traits').attr("class", "btn-large disabled styled")      

    $.get('/calculate_keypoints/', function(data){
        data = JSON.parse(data);
        console.log(data)
        if (data['media_type']==='video'){           
            if ($('#big_image').length) {
                $('#big_image').detach()
            }
            if ($('#video').length==0) {
                $('#media').append('<video id="video" preload="none" controls></video>')
            }    
            $('#video').attr("src", data['image_url'])
        }    
        else {
            if ($('#video').length) {
                $('#video').detach()
            }
            if ($('#big_image').length==0) {
                $('#media').append('<img id="big_image"/>')
            }    
            $('#big_image').attr("src", data['image_url'])
        }
    })


})

$('#download_image').click(function(){
    cur_button = 'download_image'
})   

$('#download_keypoints').click(function(){
    cur_button = 'download_keypoints'
})

$('#predict_traits_any').click(function(){

    cur_button = 'predict_traits_any'
    traits_is_predicted = true

    
    $('#refresh_image').attr("class", "btn-large disabled styled")
    $('#calculate').attr("class", "btn-large disabled styled")
    $('#download_image').attr("class", "btn-large disabled styled")
    $('#download_keypoints').attr("class", "btn-large disabled styled")    
    $('#predict_traits_any').attr("class", "btn-large disabled styled")
    $('#predict_traits_orlovskaya').attr("class", "btn-large disabled styled")    
    $('#download_traits').attr("class", "btn-large disabled styled")      

    $.get('/predict_traits_any/', function(data){
        data = JSON.parse(data)
        
        if ($('#traits_table').length) $('#traits_table').detach()
        if ($('#traits_error_message').length) $('#traits_error_message').detach()

        if (data.hasOwnProperty('error')) {
            $('#traits_table_place').append('<div id="traits_error_message">' + data['error'] + '</div>')  
            return
        }    

        var table = $('<table class="bordered striped highlight centered responsive-table" id="traits_table"/>')
        var head = $('<thead><tr><th>номер стати</th><th>название стати</th><th>значение</th></tr></thead>')        
        table.append(head)
        var body = $('<tbody/>')
        var i = 1
        for (const [key, val] of Object.entries(data)) {
              var row = $('<tr/>')
              row.append('<td>' + i++ + '</td>')              
              row.append('<td>' + key + '</td>')
              row.append('<td>' + val + '</td>')
              body.append(row)
        }                      
        table.append(body)
        $('#traits_table_place').append(table)       
    })

})


$('#predict_traits_orlovskaya').click(function(){

    cur_button = 'predict_traits_orlovskaya'
    traits_is_predicted = true

    
    $('#refresh_image').attr("class", "btn-large disabled styled")
    $('#calculate').attr("class", "btn-large disabled styled")
    $('#download_image').attr("class", "btn-large disabled styled")
    $('#download_keypoints').attr("class", "btn-large disabled styled")    
    $('#predict_traits_any').attr("class", "btn-large disabled styled")
    $('#predict_traits_orlovskaya').attr("class", "btn-large disabled styled")    
    $('#download_traits').attr("class", "btn-large disabled styled")      

    $.get('/predict_traits_orlovskaya/', function(data){
        data = JSON.parse(data)
        
        if ($('#traits_table').length) $('#traits_table').detach()
        if ($('#traits_error_message').length) $('#traits_error_message').detach()

        if (data.hasOwnProperty('error')) {
            $('#traits_table_place').append('<div id="traits_error_message">' + data['error'] + '</div>')  
            return
        }    

        var table = $('<table class="bordered striped highlight centered responsive-table" id="traits_table"/>')
        var head = $('<thead><tr><th>номер стати</th><th>название стати</th><th>значение</th></tr></thead>')        
        table.append(head)
        var body = $('<tbody/>')
        var i = 1
        for (const [key, val] of Object.entries(data)) {
              var row = $('<tr/>')
              row.append('<td>' + i++ + '</td>')              
              row.append('<td>' + key + '</td>')
              row.append('<td>' + val + '</td>')
              body.append(row)
        }                      
        table.append(body)
        $('#traits_table_place').append(table)       
    })

})

$(document).on("ajaxSend", function() {

    $("#preloader").css('visibility', 'visible')

}).on("ajaxStop", function(){

    $("#preloader").css('visibility', 'hidden')

    if (cur_button === 'refresh_image') {
        $('#refresh_image').attr("class", "waves-effect btn-large styled")
        $('#calculate').attr("class", "waves-effect btn-large styled")
        $('#download_image').attr("class", "btn-large disabled styled")
        $('#download_keypoints').attr("class", "btn-large disabled styled")
        $('#predict_traits_any').attr("class", "waves-effect btn-large styled")
        $('#predict_traits_orlovskaya').attr("class", "waves-effect btn-large styled")        
        $('#download_traits').attr("class", "btn-large disabled styled")          
    }
    else {
        if ((cur_button === 'calculate')||(cur_button === 'predict_traits_any')||(cur_button === 'predict_traits_orlovskaya')) {
            $('#refresh_image').attr("class", "waves-effect btn-large styled")
            $('#calculate').attr("class", "waves-effect btn-large styled")
            if (keypoints_is_calculated) {
                $('#download_image').attr("class", "waves-effect btn-large styled")
                $('#download_keypoints').attr("class", "waves-effect btn-large styled")
            }    
            $('#predict_traits_any').attr("class", "waves-effect btn-large styled")
            $('#predict_traits_orlovskaya').attr("class", "waves-effect btn-large styled")            
            if (traits_is_predicted) $('#download_traits').attr("class", "waves-effect btn-large styled")              
        }
    }

})

