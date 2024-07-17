import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from .utilities import get_si_prefix_base10, get_si_prefix_symbol

def set_cbar(fig: matplotlib.figure.Figure, cax: matplotlib.image.AxesImage, observable: str, unit: str, rescale: str, fmt: str, fmt_default: str) -> None:
    try:
        fn_fmt = lambda x, pos: ('{' + fmt + '}').format(x * get_si_prefix_base10(rescale))
    except ValueError:
        fn_fmt = lambda x, pos: ('{' + fmt_default + '}').format(x * get_si_prefix_base10(rescale))
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

