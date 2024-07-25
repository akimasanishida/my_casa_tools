import os
import numpy as np
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from .Image import Image
from .PlotConfig import PlotConfig
from .utilities import unitDict, get_pret_dir_name
from .matplotlib_helper import set_cbar, set_axes_options

def imshow(imagename: str, **kwargs) -> None:
    """Rastering image with matplotlib from CASA style image file.
    
    Create image from CASA style image file (`*.image`, `*.image.pbcor`,...) with matplotlib. You can save the image as common format (`*.png`, `*.jpg`,...).
    Only intensity image is supported now.

    Args:
        imagename (str): CASA style image file.
        **kwargs: Plot config keywords.
    """
    config = PlotConfig()
    config.__dict__.update(kwargs)
    imagename = get_pret_dir_name(imagename)
    # open image
    img = Image(imagename, config.width, config.height)
    config.width, config.height = img.get_fig_size()
    img.convert_axes_unit(config.axesunit)
    # plot
    fig = plt.figure()
    ax = fig.add_subplot()
    cax = ax.imshow(img.img, cmap=config.cmap, aspect='equal', vmin=config.vmin, vmax=config.vmax, origin='lower')
    # beam
    if img.beam:
        beam_x = img.beam_x / np.abs(img.incr_x)
        beam_y = img.beam_y / np.abs(img.incr_y)
        beam_pos_x = config.width / 8
        beam_pos_y = config.height / 8
        ellipse = Ellipse(xy=(beam_pos_x, beam_pos_y), width=beam_x, height=beam_y, angle=90+img.beam_ang, facecolor="white",
                          edgecolor="white")
        ax.add_patch(ellipse)
    if config.title == None:
        config.title = imagename
    set_axes_options(ax, config.title, img.axisname_x + f'[{unitDict[img.axis_unit_x]}]', img.axisname_y + f'[{unitDict[img.axis_unit_y]}]',
                     *img.get_ticks(config.xtickspan, config.ytickspan, config.relative, config.ticksfmt))
    # colorbar
    set_cbar(fig, cax, img.imtype, img.im_unit, config.rescale, config.cbarfmt, ':.2f')
    # save
    if config.savename != None:
        if config.savename == '':
            config.savename = imagename + '.png'
        fig.savefig(config.savename, dpi=config.dpi)
        print(f'Saved as "{config.savename}"')
    if config.show:
        plt.show()
