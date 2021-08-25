"""
Demonstration of using `astroalign` to align two images. 

# See  https://astroalign.readthedocs.io/en/latest/ for complete documentation.

Author: Shane Burns
Date: 8/23/21, 11:51 AM
"""
#%% import needed modules

import numpy as np
import astroalign as aa
from astropy.io import fits
from astropy import stats

#%% Load images to align
hdu_list_6 = fits.open('../images/stars06_p.fits')
header_6 = hdu_list_6[0].header
image_6 = hdu_list_6[0].data
hdu_list_6.close()

hdu_list_7 = fits.open('../images/stars07_p.fits')
header_7 = hdu_list_7[0].header
image_7 = hdu_list_7[0].data
hdu_list_7.close()

#%% Find the image transformation
# The transformation is returned in the `p` object. The two objects `img_6_srcs` 
# and `img_7_srcs` give the coordinates of the sources found by the
#`astroalign.find_transform()` fucntion.
p, (img_6_srcs, img_7_srcs) = aa.find_transform(image_6, image_7)

#%% Transform the `source` image
# Unfortunatly, in version 2.4 of `astroalign` we have to convert the image data 
# type for our images to unsigned 16 bit integers (`uint16`) to make the 
# transform function work properly. We do this using the image method
# `astype('uint16')`. 
image_6_aligned, footprint = aa.apply_transform(p, image_6.astype('uint16'),                                                 image_7.astype('uint16'),                                                 fill_value=1000)

#%% Write the shifted image to a new FITS file
# Creating a new header for the file and add new keyword to the file that 
# specifies how the image was aligned.  
header_6_aligned=header_6
header_6_aligned['ALINGED'] = 'Aligned to stars07_p.fits'
header_6_aligned

fits.writeto('../images/stars06_aligned_example.fits',image_6_aligned,
            header_6_aligned,overwrite=True)




