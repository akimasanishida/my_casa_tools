import numpy as np
from .Image import Image

def imstat(imagename: str, region_mask: str, inverse_mask: bool = False):
    """
    ToDo: Now only rms can be calculated. Add all quantities of `imstat`.
    """
    img = Image(imagename)
    img_mask = Image(region_mask)
    max_mask = np.max(img_mask.img)
    min_mask = np.min(img_mask.img)
    img_mask.img = (img_mask.img - min_mask) / (max_mask - min_mask)
    if inverse_mask:
        img_mask.img = 1 - img_mask.img
    n_pix = np.sum(img_mask.img)
    img.img *= img_mask.img
    return np.sqrt(np.sum(np.square(img.img)) / n_pix)

