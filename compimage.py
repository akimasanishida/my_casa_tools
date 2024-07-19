import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker

import numpy as np
from .Image import Image
from .utilities import unitDict, get_pret_dir_name
from .matplotlib_helper import set_axes_options, set_cbar

def compimage(imagename1, imagename2, savename=None, fig_width=None, fig_height=None, cmap='jet', rescale=None, cbarfmt=':.2f', relative=True, xtickspan=1, ytickspan=1, ticksfmt=':.3f', show=True, dpi=300):
    """Compare two image

    Args:
        imagename1 (str): CASA style image file.
        imagename2 (str): CASA style image file.
        fig_width (in, optionalt): Width of creating image. `0` for original width.
        fig_height (int, optional): Height of creating image. `0` for original height.
        cmap (str): Colormap. Default is `'jet'`.
        rescale: Rescaling factor. This must be given as SI prefixies like `'milli'`.
        cbarfmt: Colorbar's format. Python's format function style. Default is `':.2f'`.
        relative (bool, optional): If `true`, the coordination of ticks will be relative. If `false`, it will be global.
        xtickspan (int, optional): Number of ticks of x-axis. Default is 1.
        ytickspan (int, optional): Number of ticks of y-axis. Default is 1.
        ticksfmt (str, optional): Ticks' format. Python's format function style. Default is `':.3g'`.
        show: Show plot.
        dpi (int, optional): DPI of saved image. Default is `300`.
    """
    imagename1 = get_pret_dir_name(imagename1)
    imagename2 = get_pret_dir_name(imagename2)
    img1 = Image(imagename1, fig_width, fig_height)
    fig_width, fig_height = img1.get_fig_size()
    img2 = Image(imagename2, fig_width, fig_height)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fig.subplots_adjust(top=0.85)
    img1.convert_axes_unit('arcsec')
    img2.convert_axes_unit('arcsec')
    data = img1.img / (np.pi * img1.beam_x * img1.beam_y) - img2.img / (np.pi * img2.beam_x * img2.beam_y)
    vmax = np.max(data)
    vmin = np.min(data)
    vmax = max(abs(vmax), abs(vmin))
    vmin = -vmax
    cax = ax.imshow(data, cmap=cmap, origin='lower', vmax=vmax, vmin=vmin)
    set_axes_options(ax, f'{imagename1}\nv.s.\n{imagename2}', img1.axisname_x + f'[{unitDict[img1.axis_unit_x]}]',
                     img1.axisname_y + f'[{unitDict[img1.axis_unit_y]}]', *img1.get_ticks(xtickspan, ytickspan, relative, ticksfmt))
    set_cbar(fig, cax, img1.imtype, 'Jy/px^2', rescale, cbarfmt, ':.2f')
    if savename != None:
        if savename == '':
            savename = f'{imagename1}_vs_{imagename2}.png'
        fig.savefig(savename, dpi=dpi)
        print('Saved as "{}"'.format(savename))
    if show:
        plt.show()
