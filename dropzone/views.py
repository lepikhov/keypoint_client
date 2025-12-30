import json
import mimetypes
import os
import time
from urllib.parse import unquote

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Image
from .service import (delete_tmp_request, download_video_request,
                      keypoints_for_image_request, keypoints_for_video_request, traits_for_image_any_request, traits_for_image_orlovskaya_request)
from .utils import (get_current_image_url, image_prepare, image_with_keypoints, traits_short_info, traits_correct_info,
                    json_serial, keypoints_resize)

import base64
from PIL import Image as PIL_Image
import io
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'index.html', 
                  context = get_current_image_url(request.session.session_key)      
        )

def clear_db(request):
    Image.objects.all().delete()    
    return render(request, 'cleared.html')

def file_upload(request):
    if request.method == 'POST':
        my_file=request.FILES.get('file')
        if not request.session.session_key:
            request.session.create()
        Image.objects.create(image=my_file, key=request.session.session_key)  
        return HttpResponse('')
    return JsonResponse({'post':'false'})      

def update_image(request):          
    image_url = get_current_image_url(request.session.session_key)['image_url']
    media_type = 'image'
    _, extension = os.path.splitext(image_url)
    if extension in ['.mp4', '.avi', '.webm']: 
        #image_url = "media/images/video-icon.png"    
        media_type = 'video'
    return HttpResponse(json.dumps({'image_url': image_url, 'media_type': media_type}))   

def download_image(request):

    image_url = get_current_image_url(request.session.session_key)['image_url']

    _, extension = os.path.splitext(image_url)
    if extension in ['.mp4', '.avi', '.webm']: 
        filename = 'video_with_keypoints_out_' + request.session.session_key + '.mp4'
    else:
        filename = 'image_with_keypoints_out_' + request.session.session_key + '.jpg'     

    bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    filepath = os.path.join( bd, 'media/images',  filename)

    path = open(filepath, 'rb')

    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename(filename)

    return response   

def download_keypoints(request):
    bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'keypoints_' + request.session.session_key + '.json' 
    filepath = os.path.join( bd, 'media/data',  filename)
    path = open(filepath, 'r')

    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename(filename)

    return response    



def calculate_keypoints(request):  
    bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    filename = unquote(get_current_image_url(request.session.session_key)['image_url']) 
    in_filepath = bd + '/' +filename

    media_type = 'image'

    _, extension = os.path.splitext(in_filepath)

    if extension in ['.mp4', '.avi', '.webm']:    
    #videos 
            
        videofile = open(in_filepath, 'rb')

        try:
            kp = keypoints_for_video_request(videofile, request.session.session_key, extension[1:])
        except ConnectionError:
            return HttpResponse(
                json.dumps({'image_url': "media/images/horse-smile.jpg", 'media_type': media_type})
                )          

        filename = 'keypoints_' + request.session.session_key + '.json' 
        kp_filepath = os.path.join(bd, 'media/data',  filename)
        with open(kp_filepath, 'w') as jsonfile:
            json.dump(kp, jsonfile) 
       

        filename = 'video_with_keypoints_out_' + request.session.session_key + '.mp4' 
        out_filepath = os.path.join( bd, 'media/images',  filename)        

        try:
            download_video_request(out_filepath, request.session.session_key)
        except ConnectionError:
            return HttpResponse(
                json.dumps({'image_url': "media/images/horse-smile.jpg", 'media_type': media_type})
                )        

        try:
            delete_tmp_request(request.session.session_key)
        except ConnectionError:
            return HttpResponse(
                json.dumps({'image_url': "media/images/horse-smile.jpg", 'media_type': media_type})
                )           

        media_type = 'video'
        filename = 'video_with_keypoints_out_' + request.session.session_key + '.mp4'  
        return HttpResponse(
            json.dumps({'image_url': ("media/images/" + filename), 'media_type': media_type})
            ) 

    #images

    w, h = image_prepare(in_filepath)
    filename = 'tmp.jpg' 
    in_filepath = os.path.join(bd, 'media/images',  filename) 

    imgfile = open(in_filepath, 'rb')

    try:
        kp = keypoints_for_image_request(imgfile)
    except ConnectionError:
            return HttpResponse(
                json.dumps({'image_url': "media/images/horse-smile.jpg", 'media_type': media_type})
                )  

    filename = 'keypoints_' + request.session.session_key + '.json' 
    kp_filepath = os.path.join(bd, 'media/data',  filename)
    with open(kp_filepath, 'w') as jsonfile:
        json.dump(kp, jsonfile) 

    filename = unquote(get_current_image_url(request.session.session_key)['image_url']) 
    in_filepath = bd + '/' +filename          

    filename = 'image_with_keypoints_out_' + request.session.session_key + '.jpg'  
    out_filepath = os.path.join( bd, 'media/images',  filename)        

    image_with_keypoints(in_filepath, kp, out_filepath)

    return HttpResponse(
        json.dumps({'image_url': ("media/images/" + filename + '?' + str(time.time())), 'media_type': media_type})
         )       



TRAITS_CORRECT_LIST_ANY = [
    "голова", 
    "затылок",
    "шея (длина)",
    "шея выход",     
    "холка, длина", 
    "холка (высота)",    
    "лопатка",      
    "лопатка (длина)", 
    "спина",     
    "спина (длина)", 
    "поясница",     
    "круп",     
    "круп(длина)", 
    "ложные ребра", 
    "грудная клетка", 
    "предплечье",     
    "передняя бабка(длина)",     
    #"передняя бабка (угол 11)", 
    "передняя бабка (угол 12)", 
    #"бедро", 
    "голень",     
    "скакательный сустав", 
    "задняя бабка (длина)",     
    #"задняя бабка (угол 14)", 
    "задняя бабка (угол 15)", 
]

TRAITS_CORRECT_LIST_ORLOVSKAYA = TRAITS_CORRECT_LIST_ANY.copy()
TRAITS_CORRECT_LIST_ORLOVSKAYA.append('выраженность типа')

 
def predict_traits_any(request):     
    bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    filename = unquote(get_current_image_url(request.session.session_key)['image_url']) 
    in_filepath = bd + '/' +filename

    media_type = 'image'

    _, extension = os.path.splitext(in_filepath)

    if extension in ['.mp4', '.avi', '.webm']:    
    #can't predict traits for videos 
        return HttpResponse(
            json.dumps({'error': 'cannot predict traits for vodeo'})
        ) 

    #images
    imgfile = open(in_filepath, 'rb')

    try:
        traits = traits_for_image_any_request(imgfile)
    except ConnectionError:
        return HttpResponse(
            json.dumps({'error': 'server request error'})
        )              
            
    print(traits)            

    filename = 'traits_' + request.session.session_key + '.json' 
    kp_filepath = os.path.join(bd, 'media/data',  filename)
    with open(kp_filepath, 'w') as jsonfile:
        json.dump(traits, jsonfile, ensure_ascii=True) 
   
    if 'error' in traits.keys():
        return HttpResponse(json.dumps(traits))
    
    return HttpResponse(
        json.dumps(traits_correct_info(traits_short_info(traits),TRAITS_CORRECT_LIST_ANY), sort_keys=False)
    )

def predict_traits_orlovskaya(request):     
    bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    filename = unquote(get_current_image_url(request.session.session_key)['image_url']) 
    in_filepath = bd + '/' +filename

    media_type = 'image'

    _, extension = os.path.splitext(in_filepath)

    if extension in ['.mp4', '.avi', '.webm']:    
    #can't predict traits for videos 
        return HttpResponse(
            json.dumps({'error': 'cannot predict traits for vodeo'})
        ) 

    #images
    imgfile = open(in_filepath, 'rb')

    try:
        traits = traits_for_image_orlovskaya_request(imgfile)
    except ConnectionError:
        return HttpResponse(
            json.dumps({'error': 'server request error'})
        )              
            
    print(traits, TRAITS_CORRECT_LIST_ORLOVSKAYA)            

    filename = 'traits_' + request.session.session_key + '.json' 
    kp_filepath = os.path.join(bd, 'media/data',  filename)
    with open(kp_filepath, 'w') as jsonfile:
        json.dump(traits, jsonfile, ensure_ascii=True) 
   
    if 'error' in traits.keys():
        return HttpResponse(json.dumps(traits))
    
    print(traits)

    return HttpResponse(
        json.dumps(traits_correct_info(traits_short_info(traits),TRAITS_CORRECT_LIST_ORLOVSKAYA), sort_keys=False)
    )

def download_traits(request):
    bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'traits_' + request.session.session_key + '.json' 
    filepath = os.path.join( bd, 'media/data',  filename)
    path = open(filepath, 'r')

    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename(filename)

    return response

@csrf_exempt
def update_edited_image(request):
    if request.method == 'POST':
        # Получаем данные 
        image_data = request.POST.get('image_data')
        
        # Декодируем base64
        format, imgstr = image_data.split(';base64,')
        
        # Преобразуем в PIL Image
        image_bytes = base64.b64decode(imgstr)
        image = PIL_Image.open(io.BytesIO(image_bytes))
         
        bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        filename = unquote(get_current_image_url(request.session.session_key)['image_url']) 
        filepath = bd + '/' +filename        
        
        image.save(filepath)
        return update_image(request)
    
    return JsonResponse({'error': 'Invalid method'})
    
        




