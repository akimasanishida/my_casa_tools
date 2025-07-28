import skrbcr_casa_scripts as scs


# Open an existing image
image = scs.Image('image.im')

# Open an existing image with a specific area
image = scs.Image('image.im', width=100, height=100)

# Open an existing image with specifiying the center with RA and Dec
image = scs.Image('image.im', center_ra="5h30m00s", center_dec="30d00m00s")
