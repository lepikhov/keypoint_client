let cropper = null
let currentImageUrl = null
let imageLoaded = null
let currentRotation = 0 // Текущий угол поворота в градусах

Dropzone.autoDiscover = false
const myDropzone = new Dropzone('#my-dropzone', {
  dictDefaultMessage: "Перетащите медиафайл сюда или нажмите для загрузки",
  dictFallbackMessage: "Ваш браузер не поддерживает drag'n'drop загрузку файлов",
  dictFallbackText: "Пожалуйста, используйте резервную форму ниже, чтобы загрузить свои файлы",
  dictFileTooBig: "Файл слишком большой ({{filesize}}MiB). Максимальный размер: {{maxFilesize}}MiB",
  dictInvalidFileType: "Вы не можете загрузить файл данного типа",
  dictResponseError: "Сервер ответил с кодом {{statusCode}}",
  dictCancelUpload: "Отменить загрузку",
  dictCancelUploadConfirmation: "Вы уверены, что хотите отменить эту загрузку?",
  dictRemoveFile: "Удалить файл",
  dictMaxFilesExceeded: "Не не можете загрузить больше файлов",
  url: 'upload/',
  maxFiles: 1,
  maxFilesize: 200,
  acceptedFiles: "image/jpeg,image/png,image/gif,video/*",
  addRemoveLinks: true,
  timeout: 0,
  removedfile: function (file) {
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

  init: function () {
    this.on('addedfile', function (file) {
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

      // Скрываем предыдущий редактор
      document.getElementById('image-editor').style.display = 'none'
      document.getElementById('image-to-crop').style.display = 'none'
    })


    this.on("success", function (file) {
      imageLoaded = true
      // Показываем редактор после загрузки
      if (document.getElementById('enable-editor').checked) {
        init_editor(file.dataURL)
      }
    })



    this.on("maxfilesexceeded", function () {
      console.log("maxfilesexceeded")
      if (this.files[1] != null) {
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

// Инициализация редактора
function init_editor(dataURL) {
  currentImageUrl = dataURL  // URL от сервера
  if (isImageUrl(currentImageUrl)) document.getElementById('image-editor').style.display = 'block'

  // Загружаем изображение в редактор
  const image = document.getElementById('image-to-crop')
  image.src = currentImageUrl
  image.style.display = 'block'

  // Инициализируем Cropper.js
  if (cropper) {
    cropper.destroy()
  }

  cropper = new Cropper(image, {
    aspectRatio: NaN,  // Соотношение сторон (опционально)
    viewMode: 1,
    autoCropArea: 1.0,
    responsive: true,
    guides: true
  })
}

// Обработка кнопки обрезки
document.getElementById('update-edited-btn').addEventListener('click', function () {


  if (!cropper) return

  // Получаем обрезанное изображение как canvas
  const canvas = cropper.getCroppedCanvas()

  // Конвертируем в DataURL (base64)
  const croppedDataUrl = canvas.toDataURL('image/jpeg')

  $.post('/update_edited_image/', { image_data: croppedDataUrl }, function (data) {
    data = JSON.parse(data)
    if ($('#video').length) {
      $('#video').detach()
    }
    if ($('#big_image').length == 0) {
      $('#media').append('<img id="big_image"/>')
    }
    $('#big_image').attr("src", data['image_url'])
  })
})

// Кнопка отмены редактирования
document.getElementById('cancel-edit-btn').addEventListener('click', function () {
  if (cropper) {
    cropper.destroy()
    cropper = null
  }
  document.getElementById('image-editor').style.display = 'none'
})

// Кнопка отмены обрезки
document.getElementById('reset-crop-btn').addEventListener('click', function () {
  if (!cropper) return

  cropper.reset()

})


// Разрешение редактирования
document.getElementById('enable-editor').addEventListener('click', function () {
  if (!imageLoaded) return
  if (!isImageUrl(currentImageUrl)) return
  if (document.getElementById('enable-editor').checked) {
    init_editor(currentImageUrl)
    document.getElementById('image-editor').style.display = 'block'
  }    
  else {
    document.getElementById('image-editor').style.display = 'none'
  }    
})



// Поворот на 90 градусов против часовой стрелки
document.getElementById('rotate-left-btn').addEventListener('click', function () {
  rotateImage(-90)
});

// Поворот на 90 градусов по часовой стрелке
document.getElementById('rotate-right-btn').addEventListener('click', function () {
  rotateImage(90)
});

// Сброс поворота
document.getElementById('rotate-reset-btn').addEventListener('click', function () {
  if (!cropper) return


  document.getElementById('rotation-angle').textContent = '0°'
  rotateImage(-currentRotation)
  currentRotation = 0
});


// функция поворота с использованием Canvas
function rotateImage(degrees) {
  if (!cropper) return

  // Обновляем текущий угол поворота
  currentRotation += degrees
  currentRotation = (currentRotation % 360 + 360) % 360

  // Обновляем отображение
  document.getElementById('rotation-angle').textContent = currentRotation + '°'
  //document.getElementById('rotation-data').value = currentRotation;

  // Получаем текущее изображение из cropper
  const canvas = cropper.getCroppedCanvas()

  // Создаем новый canvas для поворота
  const rotatedCanvas = document.createElement('canvas')
  const ctx = rotatedCanvas.getContext('2d')

  // Устанавливаем размеры canvas для поворота
  if (degrees % 180 !== 0) {
    rotatedCanvas.width = canvas.height
    rotatedCanvas.height = canvas.width
  } else {
    rotatedCanvas.width = canvas.width
    rotatedCanvas.height = canvas.height
  }

  // Поворачиваем контекст и рисуем изображение
  ctx.translate(rotatedCanvas.width / 2, rotatedCanvas.height / 2)
  ctx.rotate(degrees * Math.PI / 180)
  ctx.drawImage(canvas, -canvas.width / 2, -canvas.height / 2)

  // Обновляем изображение в cropper
  const image = document.getElementById('image-to-crop')
  image.src = rotatedCanvas.toDataURL('image/jpeg')

  // Переинициализируем cropper с новым изображением
  cropper.destroy()
  cropper = new Cropper(image, {
    aspectRatio: NaN,
    viewMode: 1,
    autoCropArea: 1.0,
    responsive: true,
    guides: true
  })
}

function isImageUrl(url) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => resolve(true); // Image loaded successfully
    img.onerror = () => resolve(false); // Image failed to load
    img.src = url;
  });
}

