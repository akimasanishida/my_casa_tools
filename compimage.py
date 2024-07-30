import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
import numpy as np
from .PlotConfig import PlotConfig
from .Image import Image
from .utilities import unitDict, get_pret_dir_name
from .matplotlib_helper import set_axes_options, set_cbar

def compimage(imagename1, imagename2, **kwargs):
    """
    Compares two images.

    Args:
        imagename1 (str): CASA style image file.
        imagename2 (str): CASA style image file.
        **kwargs: Plot configuration keywords.
    """
    imagename1, img, config = prepare_image(imagename1, **kwargs)
    imagename2 = get_pret_dir_name(imagename2)
    img2 = Image(imagename2, config.width, config.height)
    img2.convert_axes_unit(config.axesunit)
    # plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fig.subplots_adjust(top=0.85)
    data = img1.img / (np.pi * img1.beam_x * img1.beam_y) - img2.img / (np.pi * img2.beam_x * img2.beam_y)
    config.vmax = np.max(data)
    config.vmin = np.min(data)
    config.vmax = max(abs(config.vmax), abs(config.vmin))
    config.vmin = -config.vmax
    cax = ax.imshow(data, cmap=config.cmap, origin='lower', vmax=config.vmax, vmin=config.vmin)
    set_axes_options(ax, f'{imagename1}\nv.s.\n{imagename2}', img1.axisname_x + f'[{unitDict[img1.axis_unit_x]}]',
                     img1.axisname_y + f'[{unitDict[img1.axis_unit_y]}]', *img1.get_ticks(config.xtickspan, config.ytickspan, config.relative, config.ticksfmt))
    set_cbar(fig, cax, img1.imtype, 'Jy/arcsec^2', config.rescale, config.cbarfmt, ':.2f')
    if config.savename != None:
        if config.savename == '':
            config.savename = f'{imagename1}_vs_{imagename2}.png'
        fig.savefig(config.savename, dpi=config.dpi)
        print('Saved as "{}"'.format(config.savename))
    if config.show:
        plt.show()

