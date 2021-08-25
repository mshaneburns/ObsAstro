"""
Demonstration of using `photoutils` to do aperture photometry.

See the https://photutils.readthedocs.io for 
more complete documentation. 

Author: Shane Burns
Date: 7/30/21, 4:28 PM
"""
#%% import needed modules
import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder
from photutils.aperture import CircularAperture
from photutils.aperture import CircularAnnulus
from photutils.aperture import aperture_photometry
from astropy.io import ascii

def get_magnitude(flux,zmag=25.0):
    return -2.5*np.log10(flux) + zmag

#%% read an example FITS file
hdu_list = fits.open('../images/stars10_p.fits')

print('Print HDUs in file:')
hdu_list.info()
print('\n')

imheader = hdu_list[0].header
imdata = hdu_list[0].data
hdu_list.close()

#%% get image background statistics
mean, median, std = sigma_clipped_stats(imdata, sigma=3.0)
print(f'Image Background: mean = {mean:.5g}, median = {median:.5g}, standard deviation = {std:.3g}\n') 

seeing = 6.0

#%% find the sources
daofind = DAOStarFinder(fwhm=seeing,sky=median,threshold=5.*std)
sources=daofind.find_stars(imdata-median)

print('\nPrint source locations:')
sources['id','xcentroid','ycentroid'].pprint() #print out positions of sources
print('\n')

#%% perform aperture photometry
# extract source postions from table; transpose is needed for proper orientation
positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
# define the aperture
r_a = 3*seeing
apertures = CircularAperture(positions, r=r_a)
# define the annulus
r_in = r_a + 3
r_out = r_in + 15
annulus = CircularAnnulus(positions, r_in=r_in, r_out=r_out)

# plot image with apertures
y_or_n = input('Do you wish to display the image and appertures? ')
if (y_or_n[0] == 'y') or (y_or_n[0] == 'Y'):
    plt.figure(1)
    plt.clf()

    # label the sources
    mylabels = sources['id']
    for idx, txt in enumerate(mylabels):
        plt.annotate(txt,(positions[idx,0],positions[idx,1]))
    
    plt.imshow(np.log(imdata),cmap='Greys')
    apertures.plot(color='red', lw=1.5, alpha=0.5)
    annulus.plot(color='green',lw=1.5,alpha=0.5)
    plt.show()

# sum signal in source apertures
aper_ann = [apertures,annulus]
phot_table = aperture_photometry(imdata, aper_ann)

# Find the background per pixel from the annulus
print('\nMean background per pixel:')
phot_table['mean_bkg'] = phot_table['aperture_sum_1']/annulus.area
phot_table['id','mean_bkg'].pprint() 

# Compute the background signal contribution to the aperture
bkg_signal = phot_table['mean_bkg'] * apertures.area
source_counts = phot_table['aperture_sum_0'] - bkg_signal

# Compute the flux and instrumental magnitude and add info to phot_table
count_rate = source_counts/imheader['EXPTIME'] # count_rate in ADU/sec
mag = get_magnitude(count_rate)

phot_table['count_rate'] = count_rate
phot_table['mag'] = mag
print('\nPhotometry result:')
phot_table['id','count_rate','mag'].pprint()

# Write results to CSV file
phot_table.write('photometry_example.csv',format='csv',overwrite=True)
