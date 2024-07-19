import numpy as np
import matplotlib.pyplot as plt
from .Image import Image
from .matplotlib_helper import set_axes_options
from .utilities import unitDict

def detectpeak(imagename: str, width: int = None, height: int = None, cell: int = 3, mask: str = None, title=None, cmap='jet', vmin=None, vmax=None, axesunit='arcsec', relative=True, xtickspan=1, ytickspan=1, ticksfmt=':.3f') -> None:
    img = Image(imagename, width, height)
    width, height = img.get_fig_size()
    img.convert_axes_unit('arcsec')
    if cell % 2 == 0 or cell < 3 or cell > width or cell > height:
        raise ValueError('arg `cell` must be odd integer >= 3, <= width and <= height')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    cax = ax.imshow(img.img, cmap=cmap, aspect='equal', vmin=vmin, vmax=vmax, origin='lower')
    set_axes_options(ax, title, img.axisname_x + f'[{unitDict[img.axis_unit_x]}]', img.axisname_y + f'[{unitDict[img.axis_unit_y]}]',
                     *img.get_ticks(xtickspan, ytickspan, relative, ticksfmt))
    peak_x = []; peak_y = []
    if mask != None:
        img_mask = Image(mask, width, height)
        for i in range(cell // 2, height - cell // 2, 1):
            for j in range(cell // 2, width - cell // 2, 1):
                if img_mask.img[i][j] > 0 and img.img[i][j] == np.max(img.img[i - cell // 2 : i + cell // 2 + 1, j - cell // 2 : j + cell // 2]):
                    peak_x.append(j)
                    peak_y.append(i)
    else:
        for i in range(cell // 2, height - cell // 2, 1):
            for j in range(cell // 2, width - cell // 2, 1):
                if img.img[i][j] == np.max(img.img[i - cell // 2 : i + cell // 2 + 1, j - cell // 2 : j + cell // 2]):
                    peak_x.append(j)
                    peak_y.append(i)

    ax.scatter(peak_x, peak_y)
    
