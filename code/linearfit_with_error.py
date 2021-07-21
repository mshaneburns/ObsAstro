"""
Fits data to a linear function weighted by uncertainties in the data.

This script illustrates:
    - how to import data from a CSV file using numpy.loadtxt
    - how use scipy.optimize.curve_fit (with data uncertainties)
    - how to plot the data and the best fit
    - save a plot to a file
    
Author: Shane Burns
Date: 7/21/21, 3:29 PM
"""

#%% Import needed modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#%% Define the function to fit
def linearFunc(x,intercept,slope):
    y = intercept + slope * x
    return y
    
#%% Read data from a CSV file using np.loadtxt()
xdata,ydata,d_y = np.loadtxt('../data/FakeData_with_error.csv',unpack=True,delimiter=',')

#%% Find the best-fit parameters given the data
a_fit,cov=curve_fit(linearFunc,xdata,ydata,sigma=d_y,absolute_sigma=True)

#%% Compute the best-fit parameters and uncertainties
inter = a_fit[0]
slope = a_fit[1]
d_inter = np.sqrt(cov[0][0])
d_slope = np.sqrt(cov[1][1])

#%% Create and save plot
# Create a graph showing the data.
plt.errorbar(xdata,ydata,yerr=d_y,fmt='r.',label='Data')

# Compute a best fit line from the fit intercept and slope.
yfit = inter + slope*xdata

# Create a graph of the fit to the data. We just use the ordinary plot
# command for this.
plt.plot(xdata,yfit,label='Fit')

# Display a legend, label the x and y axes and title the graph.
plt.legend()
plt.xlabel('x')
plt.ylabel('y')

# Save the figure to a file
plt.savefig('FakeDataPlot_with_error_example.png',dpi=300)

# Show the graph in a new window on the users screen.
plt.show()

#%% Display the best fit values for the slope and intercept. 
print(f'The slope = {slope}, with uncertainty {d_slope}')
print(f'The intercept = {inter}, with uncertainty {d_inter}')

#%% Compute and display chi^2 statistic
chisqr = sum((ydata-linearFunc(xdata,inter,slope))**2/d_y**2)
dof = len(ydata) - 2
chisqr_red = chisqr/dof
print(f'Reduced chi^2 = {chisqr_red}')