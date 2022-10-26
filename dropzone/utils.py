import matplotlib.image as mpimg
from django.core.exceptions import ObjectDoesNotExist
from matplotlib import pyplot as plt
from skimage import io, transform

from .models import Image


def get_current_image_url():
    try: 
        image=Image.objects.latest('pk')
    except ObjectDoesNotExist:
        image = None

    if image is not None:
        return {'image_url': image.image.url}
    else:
        return {'image_url': "media/images/horse-smile.jpg"}  


def convert(x, s):
  return [s*x[0], s*(x[1])]

def image_with_keypoints(in_imgfile, kp, out_imgfile):

    #kp=list(map(lambda x: convert(x, 1804/2386), kp))  #only for emulation

    img = mpimg.imread(in_imgfile)   
    _, w, _ = img.shape 
    fig = plt.figure()
    fig_size = fig.get_size_inches()
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.imshow(img)    
    for i in range(len(kp)):        
        plt.plot(kp[i][0], kp[i][1], 'ro')
    plt.savefig(out_imgfile, dpi=w/fig_size[0])

