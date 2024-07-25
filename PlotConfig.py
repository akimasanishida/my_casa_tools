class PlotConfig:
    """General configuration for plot.
    """
    def __init__(self, savename: str = None, width: int = None, height: int = None, title: str = None, cmap: str = 'jet', vmin: float = None,
                 vmax: float = None, rescale: str = 'milli', cbarfmt: str = ':.2f', axesunit: str = 'arcsec', relative: bool = True,
                 xtickspan: int = 2, ytickspan: int = 2, ticksfmt: str = ':.3f', show: bool = True, dpi: int = 300):
        """
        Args:
            savename: Save file name. If `None`, image will not be saved. If `''`, image name will be determine by `imagename` and the format will be png.
            width: Width of creating plot.
            height: Height of creating plot.
            title: Title of the image.
            cmap: Colormap. Default is `jet`.
            vmin: Minimum of data range that the colormap covers.
            vmax: Maximum of data range that the colormap covers.
            rescale: Rescaling factor. This must be given as SI prefixies. Default is `'milli'`. None or `''` for no-rescale.
            cbarfmt: Colorbar's format. Python's format function style. Default is `':.2f'`.
            axesunit: Unit of axes. Default is `'arcsec'`.
            relative: If `true`, the coordination of ticks will be relative. If `false`, it will be global.
            xtickspan: Number of ticks of x-axis. Default is 2.
            ytickspan: Number of ticks of y-axis. Default is 2.
            ticksfmt: Ticks' format. Python's format function style. Default is `':.3f'`.
            show: Show plot.
            dpi: DPI of saved image. Default is `300`.
        """
        self.savename = savename
        self.width = width
        self.height = height
        self.title = title
        self.cmap = cmap
        self.vmin = vmin
        self.vmax = vmax
        self.rescale = rescale
        self.cbarfmt = cbarfmt
        self.axesunit = axesunit
        self.relative = relative
        self.xtickspan = xtickspan
        self.ytickspan = ytickspan
        self.ticksfmt = ticksfmt
        self.show = show
        self.dpi = dpi
