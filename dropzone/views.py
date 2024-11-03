import json
import mimetypes
import os
import time
from urllib.parse import unquote

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Image
from .service import (delete_tmp_request, download_video_request,
                      keypoints_for_image_request, keypoints_for_video_request, traits_for_image_request)
from .utils import (get_current_image_url, image_prepare, image_with_keypoints, traits_short_info,
                    json_serial, keypoints_resize)



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


 
def predict_traits(request):     
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
        traits = traits_for_image_request(imgfile)
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
        json.dumps(traits_short_info(traits))
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
        




