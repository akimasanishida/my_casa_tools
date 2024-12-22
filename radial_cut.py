from math import radians, cos, sin, ceil, sqrt
import numpy as np
from .Image import Image

def radial_cut(img: Image, azimuth: float, beam_factor: float = 0.5) -> tuple:
    """
    Radial line cut of the image along the specified azimuth angle from the center.

    Args:
        img (Image): The Image object.
        azimuth (float): The azimuth angle in degrees.
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
    azimuth_rad = radians(azimuth - 270)

    # Initialize the line cut
    line_r = []
    line_mean = []
    line_std = []

    # Define the unit direction vector for the given azimuth
    direction_x = cos(azimuth_rad)
    direction_y = sin(azimuth_rad)

    # Maximum distance to sample (avoid stepping out of the image)
    # max_distance = min(center_x, center_y, img.width - center_x, img.height - center_y)

    # Loop over points along the line
    step = 0
    search_range = int(sqrt(sampling_size ** 2 + sampling_size ** 2) / 2 + 1)
    while True:
        # Calculate the current position
        x = int(center_x + step * direction_x)
        y = int(center_y + step * direction_y)
        rect_center = np.array([x, y])

        if x < 0 or x >= img.width or y < 0 or y >= img.height:
            break

        line_r.append(step * np.abs(img.incr_x))

        v_para = np.array([direction_x, direction_y]) * sampling_size * 0.5
        v_perp = np.array([-direction_y, direction_x]) * beam_size * 0.5
        verts = [
            rect_center + v_para + v_perp,
            rect_center + v_para - v_perp,
            rect_center - v_para - v_perp,
            rect_center - v_para + v_perp,
        ]
        edges = [
            verts[1] - verts[0],
            verts[2] - verts[1],
            verts[3] - verts[2],
            verts[0] - verts[3],
        ]

        def cross(a, b):
            return a[0] * b[1] - a[1] * b[0]

        # Append the pixel value to the line
        sample = []
        # if step == 0: 0 else -search_range
        for i in range(-search_range, search_range + 1):
            for j in range(-search_range, search_range + 1):
                px = x + i
                py = y + j
                inside = True
                for k in range(4):
                    edge = edges[k]
                    vp = np.array([px, py]) - verts[k]
                    if cross(edge, vp) > 0:
                        inside = False
                        break
                if inside and 0 <= px < img.width and 0 <= py < img.height:
                    sample.append(img.img[py, px])

        if sample:
            line_mean.append(np.mean(sample))
            line_std.append(np.std(sample))
        else:
            line_mean.append(None)
            line_std.append(None)

        step += sampling_size

    return np.array(line_r), np.array(line_mean), np.array(line_std)
