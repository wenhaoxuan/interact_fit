import numpy as np
from scipy.optimize import curve_fit
import pytest
from data_model import Data, Model, Fit
from plot_data import MakePlot
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def test_fit():
    """Tests to make sure the scipy fit works as intended
    
    """
    # Makes data where y = 5x^2 + x, no error
    x_data = np.linspace(1,10,10) 
    y_data = 5*x_data**2 + x_data
    y_err = np.ones_like(x_data) * 0.1

    # Generate a guess for a quadratic
    guess = np.zeros(3)

    # Create the data and model objects
    d = Data(x_data, y_data, y_err)
    m = Model('poly', guess)

    # Expected output
    popt_expected = [0, 1, 5]

    # Perform the fit
    fit_obj = Fit(d, m)

    assert fit_obj.popt[0] == pytest.approx(popt_expected[0], abs=1e-3)
    assert fit_obj.popt[1] == pytest.approx(popt_expected[1], abs=1e-3)
    assert fit_obj.popt[2] == pytest.approx(popt_expected[2], abs=1e-3)

    print('Fit quadratic as expected')


def test_change_degree():
    # Create a model, defauls to degree 4
    m = Model('poly')
    m.change_degree(2)

    assert len(m.init_guess) == 3
    assert m.poly_deg == 2

    print('Changed degree to 2')


def test_make_plot():
    """Tests to generate a full plot

    
    """
    # Makes a linear dataset with some randomness in y
    x_data = np.linspace(1,10,10) 
    y_data = x_data + np.random.rand(10)
    y_err = np.ones_like(x_data) * 0.1

    # Fitting with a fourth order polynomial
    guess = np.zeros(4)
    d = Data(x_data,y_data,y_err)
    m = Model('poly', guess)

    fit_obj = Fit(d, m)
    MakePlot(d, m, fit_obj)


test_fit() 
test_change_degree()
test_make_plot()
