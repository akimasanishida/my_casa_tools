import numpy as np
from .Image import Image

def imstat(imagename: str, width: int=None, height: int=None, unit: str = 'beam', region_mask: str=None, inverse_mask: bool=False):
    """
    Alternative version of imstat.
    """
    img = Image(imagename, width, height)
    img.convert_axes_unit('arcsec')
    if unit == 'beam':
        unit_area = 1
    elif unit == 'arcsec':
        unit_area = np.pi * img.beam_x * img.beam_y
    else:
        raise ValueError('Arg `unit` must be `\'beam\'` or `\'arcsec\'`.')
    img.img /= unit_area
    ret = {}
    width, height = img.get_fig_size()
    ret['unit'] = img.im_unit
    ret['all'] = {}
    ret['all']['max'] = np.max(img.img)
    ret['all']['min'] = np.min(img.img)
    ret['all']['sum'] = np.sum(img.img)
    ret['all']['sumsq'] = np.sum(np.square(img.img))
    ret['all']['mean'] = np.mean(img.img)
    ret['all']['sigma'] = np.var(img.img, ddof=1)
    ret['all']['rms'] = np.sqrt(ret['all']['sumsq'] / img.img.size)
    # process mask
    if region_mask != None:
        img_mask = Image(region_mask, width, height)
        max_mask = np.max(img_mask.img)
        # min_mask = np.min(img_mask.img)
        # img_mask.img = (img_mask.img - min_mask) / (max_mask - min_mask)
        if inverse_mask:
            img_mask.img = max_mask - img_mask.img
        data = []
        for i in range(height):
            for j in range(width):
                if img_mask.img[i][j] == 1:
                    data.append(img.img[i][j])
        data = np.array(data)
        ret['masked'] = {}
        ret['masked']['max'] = np.max(data)
        ret['masked']['min'] = np.min(data)
        ret['masked']['sum'] = np.sum(data)
        ret['masked']['sumsq'] = np.sum(np.square(data))
        ret['masked']['mean'] = np.mean(data)
        ret['masked']['sigma'] = np.var(data, ddof=1)
        ret['masked']['rms'] = np.sqrt(ret['masked']['sumsq'] / data.size)
        ret['psnr'] = ret['all']['max'] / ret['masked']['rms']
    return ret

