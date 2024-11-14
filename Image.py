import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from casatasks import imval, imhead
from .utilities import unitConvDict

class Image:
    """Image class for my_tools
    """

    def __init__(self, imagename, width: int = None, height: int = None):
        """
        Initializes the Image class with the provided image name, width, and height.

        Args:
            imagename: CASA style image file path.
            width: Width of area to open. Default to None.
            height: Height of area to open. Default to None.
        """
        # info (imhead)
        self.imagename = imagename
        self.inform = imhead(imagename=imagename)
        if self.inform is None or not isinstance(self.inform, dict):
            raise ValueError(f'Failed to retrieve image inform from "{imagename}".')

        self.width = self.inform['shape'][0]
        self.height = self.inform['shape'][1]
        self.nhz = self.inform['shape'][3]
        if self.nhz > 1:
            self.is_cube = True
        else:
            self.is_cube = False

        self.fig_width = width
        self.fig_height = height
        if self.width is None or self.height is None:
            raise ValueError(f'Invalid image shape for "{imagename}".')

        self.axisname_x = self.inform['axisnames'][0]
        self.axisname_y = self.inform['axisnames'][1]
        self.incr_x = self.inform['incr'][0]
        self.incr_y = self.inform['incr'][1]
        self.incr_hz = self.inform['incr'][3]
        self.beam = True
        try:
            self.beam_x = self.inform['restoringbeam']['major']['value']
            self.beam_y = self.inform['restoringbeam']['minor']['value']
            self.beam_ang = self.inform['restoringbeam']['positionangle']['value']
        except KeyError:
            self.beam = False
        self.imtype = self.inform['imagetype']
        self.im_unit = self.inform['unit']
        self.axis_unit_x = self.inform['axisunits'][0]
        self.axis_unit_y = self.inform['axisunits'][1]
        # figure size
        if self.fig_width is None or self.fig_width <= 0 or self.fig_width > self.width:
            self.fig_width = self.width
        if self.fig_height is None or self.fig_height <= 0 or self.fig_height > self.height:
            self.fig_height = self.height
        left = (self.width - self.fig_width) // 2
        right = (self.width + self.fig_width) // 2 - 1
        bottom = (self.height - self.fig_height) // 2
        top = (self.height + self.fig_height) // 2 - 1
        # data (imval)
        _ = imval(imagename=imagename, box=f'{left}, {bottom}, {right}, {top}')
        if self.is_cube:
            self.img = np.array(_['data']).transpose(2, 1, 0)
        else:
            self.img = np.array(_['data']).transpose()

    def get_fig_size(self) -> (int, int):
        """
        Returns size of the figure.
        
        Returns:
            (width: int, height: int)
        """
        return self.fig_width, self.fig_height

    def convert_axes_unit(self, unit: str):
        """
        Converts the unit of the axes

        Args:
            unit: The new unit.
        """
        self.incr_x *= unitConvDict[(self.axis_unit_x, unit)]
        self.incr_y *= unitConvDict[(self.axis_unit_y, unit)]
        self.axis_unit_x = unit
        self.axis_unit_y = unit

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
        _fmt = '{' + fmt + '}'
        xmid = self.fig_width / 2; ymid = self.fig_height / 2
        xlini = -self.fig_width / 2 * self.incr_x; ylini = -self.fig_height / 2 * self.incr_y
        xlmid = 0; ylmid = 0
        xlfin = self.fig_width / 2 * self.incr_x; ylfin = self.fig_height / 2 * self.incr_y
        if relative:
            xticks_label = [xlini, 0.]
            yticks_label = [ylini, 0.]
        else:
            xticks_label = [xlini, 0.]
            yticks_label = [ylini, 0.]
        xticks = [0, xmid]
        yticks = [0, ymid]
        for i in range(1, xtickspan + 1):
            xticks.append(xmid * i / (xtickspan + 1))
            xticks_label.append((xlmid - xlini) * i / (xtickspan + 1) + xlini)
            xticks.append((xmid - self.fig_width) * i / (xtickspan + 1) + self.fig_width)
            xticks_label.append((xlmid - xlfin) * i / (xtickspan + 1) + xlfin)
        for i in range(1, ytickspan + 1):
            yticks.append(ymid * i / (ytickspan + 1))
            yticks_label.append((ylmid - ylini) * i / (ytickspan + 1) + ylini)
            yticks.append((ymid - self.fig_height) * i / (ytickspan + 1) + self.fig_height)
            yticks_label.append((ylmid - ylfin) * i / (ytickspan + 1) + ylfin)
        for i, s in enumerate(xticks_label):
            xticks_label[i] = _fmt.format(s)
        for i, s in enumerate(yticks_label):
            yticks_label[i] = _fmt.format(s)
        return xticks, xticks_label, yticks, yticks_label
