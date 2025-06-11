from math import sqrt, ceil, cos, radians, sin
import numpy as np
from .Image import Image


def radial_profile(
    img: Image,
    azimuth: tuple = None,
    beam_factor: float = 0.5,
    inc: float = 0.0,         # inclination in degrees (0 = face-on)
    PA: float = 0.0           # position angle in degrees (east of north)
) -> tuple:
    """
    Extract a radial profile from an image.

    Args:
        img (Image): The Image object.
        azimuth (tuple): The azimuth range angle in degrees. If None, all azimuth angles are considered.
        beam_factor (float, optional): Sampling size based on the beam size. Defaults to 0.5.
        inc (float, optional): The inclination angle in degrees. Defaults to 0.0.
        PA (float, optional): The position angle in degrees. Defaults to 0.0.

    Returns:
        tuple: A tuple of three numpy arrays:
            - The radial distance from the center.
            - The mean intensity.
            - The standard deviation of the intensity.
    """
    # Calculate the center of the image
    center_x = img.center_pix[0]
    center_y = img.center_pix[1]

    # Calculate the beam size
    if not img.beam:
        raise ValueError("The image does not have a beam size.")
    img.convert_axes_unit('arcsec')
    beam_maj = img.beam[0] / np.abs(img.incr_x)
    beam_min = img.beam[1] / np.abs(img.incr_y)

    # Determine the larger beam size (to define the sampling step and width)
    beam_size = max(beam_maj, beam_min)
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

    # Convert inclination and PA to radians
    inc_rad = radians(inc)
    PA_rad = radians(PA)

    for i in range(len(img.data)):
        for j in range(len(img.data[0])):
            # Shift to center
            dx = j - center_x
            dy = i - center_y

            # Rotate by -PA
            x_rot = dx * cos(-PA_rad) - dy * sin(-PA_rad)
            y_rot = dx * sin(-PA_rad) + dy * cos(-PA_rad)

            # Deproject y
            y_deproj = y_rot / cos(inc_rad)

            # Deprojected radius
            r = sqrt(x_rot**2 + y_deproj**2)

            rad = np.degrees(np.arctan2(y_deproj, x_rot) % (2 * np.pi))
            if is_in_azimuth_range(rad, azimuth):
                idx = int(r / sampling_size)
                if idx >= len(line_r):
                    continue
                sample[idx].append(img.data[i, j])

    for i, s in enumerate(sample):
        # print(f'Line {i}: {np.max(s)}')
        if not s:
            line_mean.append(0)
            line_std.append(0)
        else:
            line_mean.append(np.mean(s))
            line_std.append(np.std(s))

    return np.array(line_r) * abs(img.incr_x), np.array(line_mean), np.array(line_std)
