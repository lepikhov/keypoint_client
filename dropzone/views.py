import json
import mimetypes
import os
import time
from urllib.parse import unquote

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Image
from .service import keypoints_request
from .utils import get_current_image_url, image_with_keypoints


def home(request):
    return render(request, 'index.html', context = get_current_image_url())

def file_upload(request):
    if request.method == 'POST':
        my_file=request.FILES.get('file')
        Image.objects.all().delete()
        Image.objects.create(image=my_file)
        return HttpResponse('')
    return JsonResponse({'post':'false'})      

def update_image(request):               
    return HttpResponse(get_current_image_url()['image_url'])   

def download_image(request):
    bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'image_with_keypoints_out.jpg' 
    filepath = os.path.join( bd, 'media/images',  filename)
    path = open(filepath, 'rb')

    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename(filename)

    return response   

def download_keypoints(request):
    bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'keypoints.json' 
    filepath = os.path.join( bd, 'media/data',  filename)
    path = open(filepath, 'r')

    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename(filename)

    return response    



def calculate_keypoints(request):  
    bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    filename = unquote(get_current_image_url()['image_url']) 
    in_filepath = bd + '/' +filename

    imgfile = open(in_filepath, 'rb')

    try:
        kp = keypoints_request(imgfile)
    except ConnectionError:
        return HttpResponse("media/images/horse-smile.jpg")   

    filename = 'keypoints.json' 
    kp_filepath = os.path.join( bd, 'media/data',  filename)
    with open(kp_filepath, 'w') as jsonfile:
        json.dump(kp, jsonfile) 

    filename = 'image_with_keypoints_out.jpg' 

    out_filepath = os.path.join( bd, 'media/images',  filename)        

    image_with_keypoints(in_filepath, kp, out_filepath)

    return HttpResponse("media/images/" + filename + '?' + str(time.time()))       





        




