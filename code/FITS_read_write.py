"""
Read and write FITS files.

This script illustrates: 
    - how to read and write FITS files
    - display and modify header information 
    - display the image data
    - write a new FITS file with the modified header
    
Author: Shane Burns
Date: 7/9/21, 10:24 AM
"""

# Import required modules
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# Open FITS file and load primary HDU header and data into local variables
image_file_path = '../images/M51_R_p.fits'
hdu_list = fits.open(image_file_path)
print("\n")
hdu_list.info()
print("\n")

header_data = hdu_list[0].header
image_data = hdu_list[0].data

hdu_list.close()

# Modify header OBJECT keyword
print(f"Original OBJECT name: {header_data['OBJECT']}")

header_data['OBJECT'] = 'M51 Whirlpool Galaxy'

print(f"New OBJECT name: {header_data['OBJECT']}")
print("\n")

# Display image data
plt.clf()
plt.imshow(image_data, cmap='gray',vmin=50,vmax=250) 
plt.colorbar()
plt.show()

# Write a new FITS file with modified OBJECT keyword
new_file_path = '../images/M51File_example.fits'
fits.writeto(new_file_path, image_data, header_data, overwrite=True)