import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
from .PlotConfig import PlotConfig
from .Image import Image
from .matplotlib_helper import set_axes_options, set_cbar
from .utilities import unitDict, get_pret_dir_name

def detectpeak(imagename: str, mask: str = None, markercolor: str = None, **kwargs) -> None:
    """
    Detects peaks in an image.

    Args:
        imagename (str): The name of the image file.
        mask (str, optional): The mask file. Defaults to None.
        markercolor (str, optional): The color of the peak markers. Defaults to None.
        **kwargs: Plot configuration keywords.
    """
    imagename, img, config = prepare_image(imagename, **kwargs)
    # plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    cax = ax.imshow(img.img, cmap=config.cmap, aspect='equal', vmin=config.vmin, vmax=config.vmax, origin='lower')
    if config.title is None:
        config.title = f'Detected peak of {imagename}'
    set_axes_options(ax, config.title, img.axisname_x + f'[{unitDict[img.axis_unit_x]}]', img.axisname_y + f'[{unitDict[img.axis_unit_y]}]',
                     *img.get_ticks(config.xtickspan, config.ytickspan, config.relative, config.ticksfmt))
    # beam and search cell size
    img.convert_axes_unit('arcsec')
    beam_x = img.beam_x / np.abs(img.incr_x)
    beam_y = img.beam_y / np.abs(img.incr_y)
    beam_pos_x = config.width / 8
    beam_pos_y = config.height / 8
    beam_ang = (90 + img.beam_ang) * np.pi / 180
    cell_width = int(np.sqrt((beam_x * np.cos(beam_ang)) ** 2 + (beam_x * np.sin(beam_ang)) ** 2) + 1)
    cell_height = int(np.sqrt((beam_x * np.sin(beam_ang)) ** 2 + (beam_y * np.cos(beam_ang)) ** 2) + 1)
    # detect peak
    peak_x = []; peak_y = []
    peak = {}
    if mask != None:
        img_mask = Image(mask, config.width, config.height)
        for i in range(cell_height // 2, config.height - cell_height // 2, 1):
            for j in range(cell_width // 2, config.width - cell_width // 2, 1):
                if img_mask.img[i][j] > 0 and img.img[i][j] == np.max(img.img[i - cell_height // 2 : i + cell_height // 2 + 1,
                                                                              j - cell_width // 2 : j + cell_width // 2]):
                    peak_x.append(j)
                    peak_y.append(i)
                    peak[(j, i)] = img.img[i][j]
    else:
        for i in range(cell // 2, config.height - cell // 2, 1):
            for j in range(cell // 2, config.width - cell // 2, 1):
                if img.img[i][j] == np.max(img.img[i - cell // 2 : i + cell // 2 + 1, j - cell // 2 : j + cell // 2]):
                    peak_x.append(j)
                    peak_y.append(i)
                    peak[(j, i)] = img.img[i][j]
    # plot
    ax.scatter(peak_x, peak_y, color=markercolor)
    ellipse = Ellipse(xy=(beam_pos_x, beam_pos_y), width=beam_x, height=beam_y, angle=90+img.beam_ang, facecolor="white",
                      edgecolor="white")
    rectangle = Rectangle((beam_pos_x - cell_width / 2, beam_pos_y - cell_height / 2), cell_width, cell_height, facecolor="black", edgecolor="black")
    ax.add_patch(rectangle)
    ax.add_patch(ellipse)
    # colorbar
    set_cbar(fig, cax, img.imtype, img.im_unit, config.rescale, config.cbarfmt, ':.2f')
    print(config.__dict__)
    if config.savename != None:
        if config.savename == '':
            config.savename = f'{imagename}_detectpeak.png'
        fig.savefig(config.savename, dpi=config.dpi)
        print(f'Saved as "{config.savename}"')
    if config.show:
        plt.show()
    return peak
    
