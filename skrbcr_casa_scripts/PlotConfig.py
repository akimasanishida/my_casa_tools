class PlotConfig:
    """General configuration for plot.
    """
    def __init__(self,
                 savename: str = None,
                 width: int = None,
                 height: int = None,
                 chan: int = None,
                 title: str = None,
                 cmap: str = 'jet',
                 vmin: float = None,
                 vmax: float = None,
                 cbar: str = 'common',
                 cbar_label: str = None,
                 cbar_unit: str = None,
                 cbeam: str = 'white',
                 rescale: str = 'milli',
                 cbarfmt: str = ':.2f',
                 axesunit: str = 'arcsec',
                 relative: bool = True,
                 xtickspan: int = 2,
                 ytickspan: int = 2,
                 ticksfmt: str = ':.3f',
                 show: bool = True,
                 dpi: int = 300
                 ):
        """
        Args:
            savename: Save file name. If `None`, image will not be saved. If `''`, image name will be determine by `imagename` and the format will be png.
            width: Width of creating plot.
            height: Height of creating plot.
            chan: Channel number of cube.
            title: Title of the image.
            cmap: Colormap. Default is `jet`.
            vmin: Minimum of data range that the colormap covers.
            vmax: Maximum of data range that the colormap covers.
            cbar: Colorbar range settings. Default is `'common'`. Other options are `'individual'`. If vmin or vmax is given, these values will be used primarily.
            cbar_label: Label of colorbar.
            cbar_unit: Unit of colorbar.
            cbeam: Color of beam. Default is `'white'`.
            rescale: Rescaling factor. This must be given as SI prefixies. Default is `'milli'`. None or `''` for no-rescale.
            cbarfmt: Colorbar's format. Python's format function style. Default is `':.2f'`.
            axesunit: Unit of axes. Default is `'arcsec'`.
            relative: If `true`, the coordination of ticks will be relative. If `false`, it will be global.
            xtickspan: Number of ticks of x-axis. Default is 2.
            ytickspan: Number of ticks of y-axis. Default is 2.
            ticksfmt: Ticks' format. Python's format function style. Default is `':.3f'`.
            show: Show plot. Default is `True`. If the image is a cube, this will always be `False`.
            dpi: DPI of saved image. Default is `300`.
        """
        self.savename = savename
        self.width = width
        self.height = height
        self.chan = chan
        self.title = title
        self.cmap = cmap
        self.vmin = vmin
        self.vmax = vmax
        self.cbar = cbar
        self.cbarquantity = cbar_label
        self.cbarunit = cbar_unit
        self.cbeam = cbeam
        self.rescale = rescale
        self.cbarfmt = cbarfmt
        self.axesunit = axesunit
        self.relative = relative
        self.xtickspan = xtickspan
        self.ytickspan = ytickspan
        self.ticksfmt = ticksfmt
        self.show = show
        self.dpi = dpi
