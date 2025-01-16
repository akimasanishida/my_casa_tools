import numpy as np
from .Image import Image


def detectpeak(img: Image, img_mask: Image = None) -> dict:
    """
    Detects peaks in an image.

    Args:
        img (Image): The image object.
        img_mask (Image): The mask image object. If provided, only the peaks within the mask will be detected.

    Returns:
        dict: The dictionary of detected peaks. The key is the peak index (x, y) and the value is the peak intensity.
    """
    # beam and search cell size
    img.convert_axes_unit('arcsec')
    beam_x = img.beam_x / np.abs(img.incr_x)
    beam_y = img.beam_y / np.abs(img.incr_y)
    beam_ang = (90 + img.beam_ang) * np.pi / 180
    cell_width = int(np.sqrt((beam_x * np.cos(beam_ang)) ** 2 + (beam_x * np.sin(beam_ang)) ** 2) + 1)
    cell_height = int(np.sqrt((beam_x * np.sin(beam_ang)) ** 2 + (beam_y * np.cos(beam_ang)) ** 2) + 1)

    # detect peak
    peak = {}

    if img_mask is None:
        img_mask = Image(data=np.ones((img.height, img.width)))
    for i in range(cell_height // 2, img.height - cell_height // 2, 1):
        for j in range(cell_width // 2, img.width - cell_width // 2, 1):
            if img_mask.img[i][j] > 0 and \
                    img.img[i][j] == np.max(img.img[i - cell_height // 2 : i + cell_height // 2 + 1,
                                                                          j - cell_width // 2 : j + cell_width // 2]):
                peak[(j, i)] = img.img[i][j]

    return peak
