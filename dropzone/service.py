from urllib import response

import requests
from keypoint_client.config import (SERVER_DELETE_TMP_URL,
                                    SERVER_DOWNLOAD_VIDEO_URL,
                                    SERVER_PREDICT_IMAGE_URL,
                                    SERVER_PREDICT_VIDEO_URL, 
                                    SERVER_PREDICT_IMAGE_ANY_TRAITS_URL,
                                    SERVER_PREDICT_IMAGE_ORLOVSKAYA_TRAITS_URL,
                                    SERVER_TIMEOUT)



def keypoints_for_image_request(file=None, token='12345'):

    try:
        resp = requests.put(f'{SERVER_PREDICT_IMAGE_URL}/{token}', files = {"file": file}, timeout=SERVER_TIMEOUT)
        print(resp.elapsed.total_seconds())
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        raise ConnectionError  

    if not resp.ok:
        raise ConnectionError   

    return resp.json()

def keypoints_for_video_request(file=None, token='12345', extension='mp4'):
    try:
        resp = requests.put(f'{SERVER_PREDICT_VIDEO_URL}/{extension}/{token}', 
                             files = {"file": file}, timeout=SERVER_TIMEOUT)
        print(resp.elapsed.total_seconds())
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        raise ConnectionError  

    if not resp.ok:
        print(resp.status_code)        
        raise ConnectionError   

    return resp.json()

def download_video_request(filepath=None, token='12345'):
    try:
        resp = requests.get(f'{SERVER_DOWNLOAD_VIDEO_URL}/{token}', 
                             timeout=SERVER_TIMEOUT)
        print(resp.elapsed.total_seconds())
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        raise ConnectionError  

    if not resp.ok:
        print(resp.status_code)
        raise ConnectionError   

    open(filepath, 'wb').write(resp.content)

def delete_tmp_request(token='12345'):
    #if 1:
    try:
        resp = requests.delete(f'{SERVER_DELETE_TMP_URL}/{token}', 
                             timeout=SERVER_TIMEOUT)
        print(resp.elapsed.total_seconds())
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        raise ConnectionError  

    if not resp.ok:
        print(resp.status_code)        
        raise ConnectionError   

def traits_for_image_any_request(file=None, token='12345'):

    try:
        resp = requests.put(f'{SERVER_PREDICT_IMAGE_ANY_TRAITS_URL}/{token}', files = {"file": file}, timeout=SERVER_TIMEOUT)
        print(resp.elapsed.total_seconds())
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        raise ConnectionError  

    if not resp.ok:
        raise ConnectionError   

    return resp.json()       

def traits_for_image_orlovskaya_request(file=None, token='12345'):

    try:
        resp = requests.put(f'{SERVER_PREDICT_IMAGE_ORLOVSKAYA_TRAITS_URL}/{token}', files = {"file": file}, timeout=SERVER_TIMEOUT)
        print(resp.elapsed.total_seconds())
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        raise ConnectionError  

    if not resp.ok:
        raise ConnectionError   

    return resp.json()        
