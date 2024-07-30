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
    imagename = imagename.rstrip('/')
    if config.savename == '':
        config.savename = imagename + '.png'
    img = Image(imagename, config.width, config.height)
    config.width, config.height = img.get_fig_size()
    img.convert_axes_unit(config.axesunit)
    imagename = os.path.split(imagename)[1]
    return imagename, img, config
