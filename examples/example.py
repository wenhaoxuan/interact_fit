"""Example script for how to use this package"""
from interact_fit.data_model import Data, Model, Fit
from interact_fit.plot_data import MakePlot
import numpy as np

# Change to your own data
x_data = np.linspace(1,10,10) 
y_data = x_data + np.random.rand(10)
y_err = np.ones_like(x_data) * 0.1

# The Data Object contains your input data
data_obj = Data(x_data,y_data,y_err)

# Set the order of the polynomial to fit the data with
poly_deg = 3
# Generates the polynomial model that fits the data
model_obj = Model('poly', poly_deg = poly_deg)

# Performs the fit
fit_obj = Fit(data_obj, model_obj)

# Generate the plot using the data, model, and fit
MakePlot(data_obj, model_obj, fit_obj)