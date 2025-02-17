import skrbcr_casa_scripts as scs


# The easiest but not floexible way to show an image
# You can obtain the image (PNG, JPG, etc...) by specifying the input file name
scs.lazy_raster('image.im')

# To save, just specify the output file name
scs.lazy_raster('image.im', savename='output_image.png')
# or
scs.lazy_raster('image.im', savename='')  # The output file name will be "image.png" (determined by the input file name)

# You can specify the properties of the image. Please refer to the reference of PlotConfig.
# For example,...
scs.lazy_raster('image.im', cmap='gray', vmin=0, vmax=1)

# You can also create image with more flexible way

# Import matplotlib.pyplot, which is very common plotting library in Python
import matplotlib.pyplot as plt

# Create a figure and an axis as usual in matplotlib
fig, ax = plt.subplots()

# Open input image as described in 1_open_image.py
image = scs.Image('image.im')

# Then, you can pass the axis of matplotlib and the image object to the imshow function
scs.imshow(ax, image)
# Now, you have plotted image on the axis `ax`.
# You can specify the properties of the image by passing the keyword arguments.
# However, in `imshow`, please use PlotConfig class (I know this difference is a bit confusing. I will fix this in the future).
# For example,...
scs.imshow(ax, image, cmap='gray', PlotConfig(vmin=0, vmax=1))

# The big difference between `lazy_raster` and `imshow` is that you can manage the image after plotting in `imshow`.
# For example, you can add circles on the image with using the matplotlib's functions.
from matplotlib.patches import Circle
circle = Circle((50, 50), 10, color='r', fill=False)
ax.add_patch(circle)

# Finally, you can save or show the image as you like.
fig.tight_layout()  # This makes your image tidy.
fig.savefig('output_image.png')  # Save the image as `output_image.png`.
plt.show()  # Show the image on the screen.
