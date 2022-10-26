from urllib import response

import requests
from keypoint_client.config import SERVER_TIMEOUT, SERVER_URL


def keypoints_request(file=None):

    try:
        resp = requests.post(SERVER_URL, files = {"file": file}, timeout=SERVER_TIMEOUT)
        print(resp.elapsed.total_seconds())
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        raise ConnectionError  

    if not resp.ok:
        raise ConnectionError   

    return resp.json()
