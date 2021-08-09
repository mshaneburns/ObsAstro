"""
Demonstrate using `photutils` to do aperture photometry.

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

# set-up for nice inline image display
plt.style.use('../im_disp.mplstyle') 

#%% read file
hdu_list = fits.open('../images/stars10_p.fits')

print('Print HDUs in file:')
hdu_list.info()
print('\n')

imheader = hdu_list[0].header
imdata = hdu_list[0].data
hdu_list.close()

#%% display image
plt.figure(1)
plt.clf()
plt.imshow(imdata,cmap='Greys',vmin=225,vmax=350)
plt.colorbar()
plt.show()

#%% get background statistics
mean, median, std = sigma_clipped_stats(imdata, sigma=3.0)
print(f'Full Image Background: mean = {mean:.5g}, median = {median:.5g}, standard deviation = {std:.3g}\n') 

#%% plot star profile to estimate seeing
starprofile = imdata[185:226,362:363]

plt.figure(2)
plt.clf()
plt.plot(starprofile)
plt.ylabel('Pixel value (ADU)')
plt.show()

#%% set the seeing value as estimated from plot
seeing = 5.0
#seeing = float(input('Estimated seeing (FWHM): '))

#%% find the sources
daofind = DAOStarFinder(fwhm=6.0,sky=median,threshold=5.*std)
sources=daofind.find_stars(imdata-median)

print('Print source locations:')
sources['id', 'xcentroid','ycentroid'].pprint() #print out positions of sources
print('\n')

#%% perform aperture photometry
# extract source postions from table, transpose needed for proper orientation
positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
# define aperture
r_a = 3*seeing
apertures = CircularAperture(positions, r=r_a)
# define annulus
r_in = r_a + 3
r_out = r_in + 14
annulus = CircularAnnulus(positions, r_in=r_in, r_out=r_out)

# plot image with apertures
plt.figure(3)
plt.clf()
plt.imshow(imdata,cmap='Greys',vmin=225,vmax=350)
apertures.plot(color='red', lw=1.5, alpha=0.5)
annulus.plot(color='green',lw=1.5,alpha=0.5)
plt.show()

# sum signal in source apertures
aper_ann = [apertures,annulus]
phot_table = aperture_photometry(imdata, aper_ann)
print('\n')
phot_table.pprint()

# Find the background per pixel from the annulus
mean_bkg = phot_table['aperture_sum_1']/annulus.area
mean_bkg.pprint() # The result is okay for all stars except 2 and 3 which are contaminated by star signal, and 10 which has part of the annulus cut off.

# Compute the background signal contribution to each apperture
bkg_signal = mean_bkg * apertures.area
source_counts = phot_table['aperture_sum_0'] - bkg_signal

# compute the flux and instrumental magnitude and add to phot_table
count_rate = source_counts/imheader['EXPTIME'] # count_rate in ADU/sec
mag = get_magnitude(count_rate)

phot_table['count_rate'] = count_rate
phot_table['mag'] = mag
phot_table.pprint()

phot_table.write('photometry_example.csv',format='csv',overwrite=True)

