import os
from .utilities import get_pret_dir_name
from .Image import Image
from .PlotConfig import PlotConfig


def prepare_image(imagename: str, **kwargs) -> (Image, PlotConfig):
    """
    Prepares the Image object and updates the configuration with the image dimensions.

    Args:
        imagename (str): The name of the image file.
        **kwargs: Additional keyword arguments to update the PlotConfig object.

    Returns:
        tuple: A tuple containing the prepared Image object and the updated PlotConfig object.
    """
    config = PlotConfig()
    config.__dict__.update(kwargs)
    img = Image(imagename=imagename, width=config.width, height=config.height)
    config.width, config.height = img.get_fig_size()
    img.convert_axes_unit(config.axesunit)
    imagename = get_pret_dir_name(imagename)
    return imagename, img, config
