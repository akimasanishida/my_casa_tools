import numpy as np
import matplotlib.pyplot as plt
from .PlotConfig import PlotConfig
from .Image import Image
from .matplotlib_helper import set_axes_options
from .utilities import unitDict

def detectpeak(imagename: str, mask: str = None, **kwargs) -> None:
    config = PlotConfig()
    config.__dict__.update(kwargs)
    img = Image(imagename, config.width, config.height)
    config.width, config.height = img.get_fig_size()
    img.convert_axes_unit(config.axesunit)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    cax = ax.imshow(img.img, cmap=config.cmap, aspect='equal', vmin=config.vmin, vmax=config.vmax, origin='lower')
    set_axes_options(ax, config.title, img.axisname_x + f'[{unitDict[img.axis_unit_x]}]', img.axisname_y + f'[{unitDict[img.axis_unit_y]}]',
                     *img.get_ticks(config.xtickspan, config.ytickspan, config.relative, config.ticksfmt))
    peak_x = []; peak_y = []
    if mask != None:
        img_mask = Image(mask, config.width, config.height)
        for i in range(cell // 2, config.height - cell // 2, 1):
            for j in range(cell // 2, config.width - cell // 2, 1):
                if img_mask.img[i][j] > 0 and img.img[i][j] == np.max(img.img[i - cell // 2 : i + cell // 2 + 1, j - cell // 2 : j + cell // 2]):
                    peak_x.append(j)
                    peak_y.append(i)
    else:
        for i in range(cell // 2, config.height - cell // 2, 1):
            for j in range(cell // 2, config.width - cell // 2, 1):
                if img.img[i][j] == np.max(img.img[i - cell // 2 : i + cell // 2 + 1, j - cell // 2 : j + cell // 2]):
                    peak_x.append(j)
                    peak_y.append(i)

    ax.scatter(peak_x, peak_y)
    
