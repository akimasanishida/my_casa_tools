import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from .utilities import get_si_prefix_base10, get_si_prefix_symbol

def set_cbar(fig: matplotlib.figure.Figure, cax: matplotlib.image.AxesImage, observable: str, unit: str, rescale: str, fmt: str, fmt_default: str) -> None:
    """
    Sets the colorbar for the given figure and image axes.

    Args:
        fig (matplotlib.figure.Figure): The figure to which the colorbar is added.
        cax (matplotlib.image.AxesImage): The image axes to which the colorbar is added.
        observable (str): The observable being plotted.
        unit (str): The unit of the observable.
        rescale (str): The SI prefix to rescale the colorbar.
        fmt (str): The format string for the colorbar labels.
        fmt_default (str): The default format string for the colorbar labels.
    """
    def fn_fmt(x, pos):
        try:
            return ('{' + fmt + '}').format(x * get_si_prefix_base10(rescale))
        except ValueError:
            return ('{' + fmt_default + '}').format(x * get_si_prefix_base10(rescale))
    cbar = fig.colorbar(cax, format=ticker.FuncFormatter(fn_fmt))
    cbar.set_label(f'{observable} [{get_si_prefix_symbol(rescale) + unit}]')

def set_axes_options(ax: matplotlib.axes.Axes, title: str, xlabel: str, ylabel: str, xticks, xticks_label, yticks, yticks_label):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks_label)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks_label)

