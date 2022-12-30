import matplotlib.image as mpimg
from django.core.exceptions import ObjectDoesNotExist
from matplotlib import pyplot as plt
from skimage import io, transform

from .models import Image
from PIL import Image as pi
import os


def get_current_image_url():
    try: 
        image=Image.objects.latest('pk')
    except ObjectDoesNotExist:
        image = None

    if image is not None:
        return {'image_url': image.image.url}
    else:
        return {'image_url': "media/images/horse-smile.jpg"}  

def image_prepare(imgfile):
    img = pi.open(imgfile)
    width, height = img.size
    img = img.resize((224, 224))
    #img = np.array(img)
    #img = np.expand_dims(img, 0)
    bd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'tmp.jpg' 
    filepath = os.path.join( bd, 'media/images',  filename)    
    img.save(filepath)
    return width, height

def convert(x, s):
  return [s*x[0], s*(x[1])]

def keypoints_resize(kp, width, height):
    return [[x[0]*width/224, x[1]*height/224] for x in kp]


def image_with_keypoints(in_imgfile, kp, out_imgfile):

    #kp=list(map(lambda x: convert(x, 1804/2386), kp))  #only for emulation

    img = mpimg.imread(in_imgfile)   
    h, w, _ = img.shape 
    fig = plt.figure(figsize=(6.4, 6.4*h/w))
    fig_size = fig.get_size_inches()
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.imshow(img)    
    for i in range(len(kp)):        
        plt.plot(kp[i][0], kp[i][1], 'x', color='red')
    plt.savefig(out_imgfile, dpi=w/fig_size[0])

