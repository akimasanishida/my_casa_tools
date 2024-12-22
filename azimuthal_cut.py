from math import degrees, radians
import numpy as np
from .Image import Image

def azimuthal_cut(img: Image, radius: float, beam_factor: float = 0.5) -> tuple:
    """
    Extract an azimuthal cut from an image.

    Args:
        img (Image): The Image object.
        radius (float): The radius in arcsec.
        beam_factor (float, optional): Sampling size based on the beam size. Defaults to 0.5.

    Returns:
        tuple: A tuple of three numpy arrays:
            - The azimuthal angle in degrees.
            - The mean intensity.
            - The standard deviation of the intensity.
    """
    # Calculate the center of the image
    center_x = img.width // 2
    center_y = img.height // 2

    # Calculate the beam size
    if not img.beam:
        raise ValueError("The image does not have a beam size.")
    img.convert_axes_unit('arcsec')
    beam_x = img.beam_x / np.abs(img.incr_x)
    beam_y = img.beam_y / np.abs(img.incr_y)

    # Determine the larger beam size (to define the sampling step and width)
    beam_size = max(beam_x, beam_y)
    radius_px = radius / np.abs(img.incr_x)
    sampling_rad = beam_size * beam_factor / radius_px
    sampling_deg = degrees(sampling_rad)

    # Initialize the line cut
    line_azm = np.arange(0, 360, sampling_deg)
    sample = [[] for _ in range(len(line_azm))]
    line_mean = np.zeros_like(line_azm)
    line_std = np.zeros_like(line_azm)

    r_min = radius_px - beam_size / 2
    r_max = radius_px + beam_size / 2

    for i in range(len(img.img)):
        for j in range(len(img.img[0])):
            dist = np.sqrt((j - center_x) ** 2 + (i - center_y) ** 2)
            if dist < r_min or dist > r_max:
                continue
            angle = (degrees(np.arctan2(i - center_y, j - center_x)) - 90) % 360
            idx = np.argmin(np.abs(line_azm - angle))
            sample[idx].append(img.img[i, j])

    line_mean = np.array([np.mean(s) for s in sample])
    line_std = np.array([np.std(s) for s in sample])

    return np.array(line_azm), np.array(line_mean), np.array(line_std)
