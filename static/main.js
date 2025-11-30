Dropzone.autoDiscover=false
const myDropzone= new Dropzone('#my-dropzone',{
    dictDefaultMessage:"Перетащите медиафайл сюда или нажмите для загрузки",
    dictFallbackMessage:"Ваш браузер не поддерживает drag'n'drop загрузку файлов",
    dictFallbackText:"Пожалуйста, используйте резервную форму ниже, чтобы загрузить свои файлы",
    dictFileTooBig:"Файл слишком большой ({{filesize}}MiB). Максимальный размер: {{maxFilesize}}MiB",
    dictInvalidFileType:"Вы не можете загрузить файл данного типа",
    dictResponseError:"Сервер ответил с кодом {{statusCode}}",
    dictCancelUpload:"Отменить загрузку",
    dictCancelUploadConfirmation:"Вы уверены, что хотите отменить эту загрузку?",
    dictRemoveFile:"Удалить файл",
    dictMaxFilesExceeded:"Не не можете загрузить больше файлов",
    url:'upload/',
    maxFiles:1,
    maxFilesize:200,
    acceptedFiles:"image/jpeg,image/png,image/gif,video/*", 
    addRemoveLinks:true,
    timeout:0,
    removedfile: function(file) {
      var _ref
      $('#refresh_image').attr("class", "btn-large disabled styled")
      $('#calculate').attr("class", "btn-large disabled styled")
      $('#download_image').attr("class", "btn-large disabled styled")
      $('#download_keypoints').attr("class", "btn-large disabled styled") 
      $('#predict_traits_any').attr("class", "btn-large disabled styled")
      $('#predict_traits_orlovskaya').attr("class", "btn-large disabled styled")      
      $('#download_traits').attr("class", "btn-large disabled styled")       
      return (_ref = file.previewElement) != null ? _ref.parentNode.removeChild(file.previewElement) : void 0
    },

    init: function() {
        this.on('addedfile', function(file) { 
          if (this.files.length > 1) {
            this.removeFile(this.files[0])
          }     
          $('#refresh_image').attr("class", "waves-effect btn-large styled")
          $('#calculate').attr("class", "btn-large disabled styled")
          $('#download_image').attr("class", "btn-large disabled styled")
          $('#download_keypoints').attr("class", "btn-large disabled styled")  
          $('#predict_traits_any').attr("class", "btn-large disabled styled")
          $('#predict_traits_orlovskaya').attr("class", "btn-large disabled styled")          
          $('#download_traits').attr("class", "btn-large disabled styled")               
        })
                

        this.on("maxfilesexceeded", function() {
          console.log("maxfilesexceeded")  
          if (this.files[1]!=null){
            this.removeFile(this.files[0])
          }
          $('#refresh_image').attr("class", "waves-effect btn-large styled")
          $('#calculate').attr("class", "btn-large disabled styled")
          $('#download_image').attr("class", "btn-large disabled styled")
          $('#download_keypoints').attr("class", "btn-large disabled styled") 
          $('#predict_traits_any').attr("class", "btn-large disabled styled")
          $('#predict_traits_orlovskaya').attr("class", "btn-large disabled styled")          
          $('#download_traits').attr("class", "btn-large disabled styled")            
        })       
    }

})

