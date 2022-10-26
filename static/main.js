Dropzone.autoDiscover=false;
Dropzone.prototype.defaultOptions.dictDefaultMessage = "Перетащите изображение сюда или нажмите для загрузки.";
Dropzone.prototype.defaultOptions.dictFallbackMessage = "Your browser does not support drag'n'drop file uploads.";
Dropzone.prototype.defaultOptions.dictFallbackText = "Please use the fallback form below to upload your files like in the olden days.";
Dropzone.prototype.defaultOptions.dictFileTooBig = "File is too big ({{filesize}}MiB). Max filesize: {{maxFilesize}}MiB.";
Dropzone.prototype.defaultOptions.dictInvalidFileType = "You can't upload files of this type.";
Dropzone.prototype.defaultOptions.dictResponseError = "Server responded with {{statusCode}} code.";
Dropzone.prototype.defaultOptions.dictCancelUpload = "Cancel upload";
Dropzone.prototype.defaultOptions.dictCancelUploadConfirmation = "Are you sure you want to cancel this upload?";
Dropzone.prototype.defaultOptions.dictRemoveFile = "Удалить файл";
Dropzone.prototype.defaultOptions.dictMaxFilesExceeded = "You can not upload any more files.";
const myDropzone= new Dropzone('#my-dropzone',{
    url:'upload/',
    maxFiles:1,
    maxFilesize:40,
    acceptedFiles:"image/jpeg,image/png,image/gif", 
    addRemoveLinks:true,
    /*
    init: function() {
        this.on("maxfilesexceeded", function() {
          console.log("maxfilesexceeded")  
          if (this.files[1]!=null){
            this.removeFile(this.files[0]);
          }
        });
    }
    */
    //,
    /*accept: function(file, done) {
  
    } */
    removedfile: function(file) {
      var _ref;
      $('#refresh_image').attr("class", "btn-large disabled styled")
      $('#calculate').attr("class", "btn-large disabled styled")
      $('#download_image').attr("class", "btn-large disabled styled")
      $('#download_keypoints').attr("class", "btn-large disabled styled") 
      return (_ref = file.previewElement) != null ? _ref.parentNode.removeChild(file.previewElement) : void 0;
    },

    init: function() {
        this.on('addedfile', function(file) {
          console.log("addedfile")    
          if (this.files.length > 1) {
            this.removeFile(this.files[0]);
          }     
          $('#refresh_image').attr("class", "waves-effect btn-large styled")
          $('#calculate').attr("class", "btn-large disabled styled")
          $('#download_image').attr("class", "btn-large disabled styled")
          $('#download_keypoints').attr("class", "btn-large disabled styled")     
        });
                

        this.on("maxfilesexceeded", function() {
          console.log("maxfilesexceeded")  
          if (this.files[1]!=null){
            this.removeFile(this.files[0]);
          }
          $('#refresh_image').attr("class", "waves-effect btn-large styled")
          $('#calculate').attr("class", "btn-large disabled styled")
          $('#download_image').attr("class", "btn-large disabled styled")
          $('#download_keypoints').attr("class", "btn-large disabled styled") 
        });        
    }

})

