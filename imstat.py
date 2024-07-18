import numpy as np
from .Image import Image

def imstat(imagename: str, width: int=None, height: int=None, region_mask: str=None, inverse_mask: bool=False):
    """
    ToDo: Now only rms can be calculated. Add all quantities of `imstat`.
    """
    ret = {}
    img = Image(imagename, width, height)
    width, height = img.get_fig_size()
    ret['unit'] = img.im_unit
    # process mask
    data = []
    if region_mask != None:
        img_mask = Image(region_mask)
        max_mask = np.max(img_mask.img)
        min_mask = np.min(img_mask.img)
        img_mask.img = (img_mask.img - min_mask) / (max_mask - min_mask)
        if inverse_mask:
            img_mask.img = 1 - img_mask.img
        for i in range(height):
            for j in range(width):
                if img_mask.img[i][j] == 1:
                    data.append(img.img[i][j])
    else:
        for i in range(height):
            for j in range(width):
                data.append(img.img[i][j])
    data = np.array(data)
    ret['rms'] = np.sqrt(np.sum(np.square(data)) / data.size)
    ret['max'] = np.max(data)
    ret['min'] = np.min(data)
    return ret

