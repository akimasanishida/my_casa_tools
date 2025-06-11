import numpy as np
from .utilities import unitConvDict


class Image:
    def __init__(self):
        self.imagename: str = None
        self.data: np.ndarray = None
        self.width: int = None
        self.height: int = None
        self.nchan: int = None
        self.center_radec: tuple[float, float] = None  # (RA, Dec)
        self.center_pix: tuple[float, float] = None  # (X, Y)
        self.freq0: float = None
        self.incr_x: float = None
        self.incr_y: float = None
        self.incr_hz: float = None
        self.unit_x: str = None
        self.unit_y: str = None
        self.unit_data: str = None
        self.beam: tuple[float, float, float] = None  # (major, minor, angle)

    def convert_axes_unit(self, unit: str):
        """
        Convert the axes units of the image to the specified unit.

        Args:
            unit (str): The unit to convert to (e.g., 'arcsec').
        """
        try:
            self.incr_x *= unitConvDict[(self.unit_x, unit)]
        except KeyError:
            raise ValueError(
                f"Unsupported unit conversion from {self.unit_x} to {unit}."
            )
        try:
            self.incr_y *= unitConvDict[(self.unit_y, unit)]
        except KeyError:
            raise ValueError(
                f"Unsupported unit conversion from {self.unit_y} to {unit}."
            )
        self.unit_x = unit
        self.unit_y = unit

    def get_ticks(self, xtickspan: int, ytickspan: int, relative: bool, fmt: str):
        """
        Returns x and y ticks and tick labels.

        Args:
            xtickspan (int): Span of ticks of x-axis.
            ytickspan (int): Span of ticks of y-axis.
            relative (bool): If True, ticks are relative coordinates. If False, ticks are global coordinates.
            fmt (str): Format of tick labels.

        Returns:
            xticks, xticks_label, yticks, yticks_label
        """
        _fmt = "{" + fmt + "}"
        xmid = self.width / 2
        ymid = self.height / 2
        xlini = -self.width / 2 * self.incr_x
        ylini = -self.height / 2 * self.incr_y
        xlmid = 0
        ylmid = 0
        xlfin = self.width / 2 * self.incr_x
        ylfin = self.height / 2 * self.incr_y
        if relative:
            xticks_label = [xlini, 0.0]
            yticks_label = [ylini, 0.0]
        else:
            xticks_label = [xlini, 0.0]
            yticks_label = [ylini, 0.0]
        xticks = [0, xmid]
        yticks = [0, ymid]
        for i in range(1, xtickspan + 1):
            xticks.append(xmid * i / (xtickspan + 1))
            xticks_label.append((xlmid - xlini) * i / (xtickspan + 1) + xlini)
            xticks.append(
                (xmid - self.width) * i / (xtickspan + 1) + self.width
            )
            xticks_label.append((xlmid - xlfin) * i / (xtickspan + 1) + xlfin)
        for i in range(1, ytickspan + 1):
            yticks.append(ymid * i / (ytickspan + 1))
            yticks_label.append((ylmid - ylini) * i / (ytickspan + 1) + ylini)
            yticks.append(
                (ymid - self.height) * i / (ytickspan + 1) + self.height
            )
            yticks_label.append((ylmid - ylfin) * i / (ytickspan + 1) + ylfin)
        for i, s in enumerate(xticks_label):
            xticks_label[i] = _fmt.format(s)
        for i, s in enumerate(yticks_label):
            yticks_label[i] = _fmt.format(s)
        return xticks, xticks_label, yticks, yticks_label

    def keep_stokes_chan(self, stokes: int, chan: int):
        """
        Keep only specific stokes and channel from the image data.
        This is useful for the image that has only one stokes and channel.

        Args:
            stokes (int): The Stokes parameter to keep.
            chan (int): The channel to keep.
        """
        # Check if the data has four dimensions (Stokes, Channel, Y, X)
        if not self.data.ndim == 4:
            raise ValueError(
                f"Data must be 4D (Stokes, Channel, Y, X), but got {self.data.ndim}D."
            )
        # Check if the specified stokes and channel are valid
        if stokes < 0 or chan < 0:
            raise ValueError("Stokes and channel indices must be non-negative.")
        if stokes >= self.data.shape[0]:
            raise ValueError(
                f"Stokes index {stokes} is out of bounds for data with shape {self.data.shape}."
            )
        if chan >= self.data.shape[1]:
            raise ValueError(
                f"Channel index {chan} is out of bounds for data with shape {self.data.shape}."
            )
        if self.data.ndim == 4:
            self.data = self.data[stokes, chan]
        elif self.data.ndim == 3:
            self.data = self.data[chan]
        else:
            raise ValueError(
                f"Unsupported data dimension: {self.data.ndim}. Expected 3D or 4D data."
            )