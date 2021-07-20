"""
Fits data to a linear function.

This script illustrates:
    - how to import data from a CSV file using numpy.loadtxt
    - how use scipy.optimize.curve_fit (without data uncertainties)
    - how to plot the data and the best fit
    - save a plot to a file
    
Author: Shane Burns
Date: 7/20/21, 3:29 PM
"""

#%% Import needed modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Read data from a CSV file using np.loadtxt()
xdata,ydata=np.loadtxt('../data/FakeData.csv',unpack=True,delimiter=',')

#%% Define the function to fit
def linearFunc(x,intercept,slope):
    y = intercept + slope * x
    return y
    
#%% Find the best-fit parameters given the data
a_fit,cov=curve_fit(linearFunc,xdata,ydata)
inter = a_fit[0]
slope = a_fit[1]

#%% Compute the best-fit parameter uncertainties
d_inter = np.sqrt(cov[0][0]) # uncertainty in intercept
d_slope = np.sqrt(cov[1][1]) # uncertainty in slope

#%% Create and save plot
# Create a graph showing the data.
plt.plot(xdata,ydata,'ro',label='Data')

# Compute a best fit y values from the fit intercept and slope.
yfit = inter + slope*xdata

# Create a graph of the fit to the data.
plt.plot(xdata,yfit,label='Fit')

# Display a legend, label the x and y axes and title the graph.
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Plot of data with fit')

# Save the figure to a file
plt.savefig('FakeDataFit_example.png',dpi=300)

# Show the graph in a new window on the users screen.
plt.show()

#%% Display the best fit values for the slope and intercept. 
print(f'The slope = {slope}, with uncertainty {d_slope}')
print(f'The intercept = {inter}, with uncertainty {d_inter}')