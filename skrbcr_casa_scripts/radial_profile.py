from math import sqrt, ceil
import numpy as np
from .Image import Image


def radial_profile(img: Image, azimuth: tuple = None, beam_factor: float = 0.5) -> tuple:
    """
    Extract a radial profile from an image.

    Args:
        img (Image): The Image object.
        azimuth (tuple): The azimuth range angle in degrees. If None, all azimuth angles are considered.
        beam_factor (float, optional): Sampling size based on the beam size. Defaults to 0.5.

    Returns:
        tuple: A tuple of three numpy arrays:
            - The radial distance from the center.
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
    sampling_size = ceil(beam_size * beam_factor)

    # Convert azimuth angle to radians
    # azimuth is measured from the north
    if azimuth is None:
        azimuth = (0, 359)
    azimuth = ((azimuth[0] + 90) % 360, (azimuth[1] + 90) % 360)

    def is_in_azimuth_range(angle, azimuth):
        if azimuth[0] < azimuth[1]:
            return azimuth[0] <= angle <= azimuth[1]
        else:
            return azimuth[0] <= angle or angle <= azimuth[1]

    # Initialize the line cut
    line_r = np.arange(0, min(center_x, center_y), sampling_size, dtype=float)
    line_mean = []
    line_std = []
    sample = [[] for _ in range(len(line_r))]

    for i in range(len(img.img)):
        for j in range(len(img.img[0])):
            r = sqrt((j - center_x) ** 2 + (i - center_y) ** 2)
            rad = np.degrees(np.arctan2(i - center_y, j - center_x) % (2 * np.pi))
            if is_in_azimuth_range(rad, azimuth):
                idx = int(r / sampling_size)
                if idx >= len(line_r):
                    continue
                sample[idx].append(img.img[i, j])

    for i, s in enumerate(sample):
        # print(f'Line {i}: {np.max(s)}')
        if not s:
            line_mean.append(0)
            line_std.append(0)
        else:
            line_mean.append(np.mean(s))
            line_std.append(np.std(s))

    return np.array(line_r) * abs(img.incr_x), np.array(line_mean), np.array(line_std)
