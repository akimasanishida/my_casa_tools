import os
import numpy as np
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from .Image import Image
from .utilities import unitDict
from .matplotlib_helper import set_cbar, set_axes_options

def imshow(imagename, savename=None, fig_width=None, fig_height=None, title=None, cmap='jet', vmin=None, vmax=None, rescale=None,
           cbarfmt=':.2f', axesunit='arcsec', relative=True, xtickspan=1, ytickspan=1, ticksfmt=':.3f', show=True, dpi=300) -> None:
    """Rastering image with matplotlib from CASA style image file.
    
    Create image from CASA style image file (`*.image`, `*.image.pbcor`,...) with matplotlib. You can save the image as common format (`*.png`, `*.jpg`,...).
    Only intensity image is supported now.

    Args:
        imagename (str): CASA style image file.
        savename (str, optional): Save file name. If `None`, image will not be saved. If `''`, image name will be determine by `imagename` and the format will be png.
        fig_width (in, optionalt): Width of creating image.
        fig_height (int, optional): Height of creating image.
        title (str, optional): Title of the image. If `None`, `imagename` will be used.
        cmap: Colormap. Default is `jet`.
        vmin (float, optional): minimum of data range that the colormap covers.
        vmax (float, optional): maximum of data range that the colormap covers.
        rescale: Rescaling factor. This must be given as SI prefixies like `'milli'`.
        cbarfmt: Colorbar's format. Python's format function style. Default is `':.2f'`.
        axesunit: Unit of axes. Default is `'arcsec'`.
        relative (bool, optional): If `true`, the coordination of ticks will be relative. If `false`, it will be global.
        xtickspan (int, optional): Number of ticks of x-axis. Default is 1.
        ytickspan (int, optional): Number of ticks of y-axis. Default is 1.
        ticksfmt (str, optional): Ticks' format. Python's format function style. Default is `':.3g'`.
        show: Show plot.
        dpi (int, optional): DPI of saved image. Default is `300`.

    ToDo:
        - `relative = True`: Global coordination
        - colorbar format
    """
    if imagename[-1] == '/':
        imagename = imagename[:-1]
    # open image
    img = Image(imagename, fig_width, fig_height)
    fig_width, fig_height = img.get_fig_size()
    img.convert_axes_unit(axesunit)
    xticks, xticks_label, yticks, yticks_label = img.get_ticks(xtickspan, ytickspan, relative, ticksfmt)
    # plot
    fig = plt.figure()
    ax = fig.add_subplot()
    cax = ax.imshow(img.img, cmap=cmap, aspect='equal', vmin=vmin, vmax=vmax, origin='lower')
    # beam
    if img.beam:
        beam_x = img.beam_x / np.abs(img.incr_x)
        beam_y = img.beam_y / np.abs(img.incr_y)
        beam_pos_x = fig_width / 8
        beam_pos_y = fig_height / 8
        ellipse = Ellipse(xy=(beam_pos_x, beam_pos_y), width=beam_x, height=beam_y, angle=90+img.beam_ang, facecolor="white",
                          edgecolor="white")
        ax.add_patch(ellipse)
    if title == None:
        title = imagename
    set_axes_options(ax, title, img.axisname_x + f'[{unitDict[img.axis_unit_x]}]', img.axisname_y + f'[{unitDict[img.axis_unit_y]}]',
                     xticks, xticks_label, yticks, yticks_label)
    # colorbar
    set_cbar(fig, cax, img.imtype, img.im_unit, rescale, cbarfmt, ':.2f')
    # save
    if savename != None:
        if savename == '':
            savename = imagename + '.png'
        fig.savefig(savename, dpi=dpi)
        print(f'Saved as "{savename}"')
    if show:
        plt.show()
