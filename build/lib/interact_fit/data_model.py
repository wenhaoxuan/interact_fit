"""Classes to deal with input data"""
import numpy as np
from scipy.optimize import curve_fit

class Data(object):
    """Class for input data

    Stores input data from user

    Args:
        x (array): x data
        y (array): y data
        yerr (array): errors on y data
        mask (array): True where to include data, False otherwise
    """

    def __init__(self, x, y, yerr, mask = []):
        self.x = x
        self.y = y
        self.yerr = yerr
        if len(mask) == 0:
            self.mask = np.ones_like(x).astype(bool)
        else:
            self.mask = mask


class Model(object):
    """Class for model

    Generates a model for fitting the data. Currently supports polynomials of arbitrary degreee

    Args:
        function_type (string): type of fitting function. Options are: poly
        init_guess (list): initial guesses for fit
        poly_deg (int): degree of the polynomial
    """

    def __init__(self, function_type, init_guess=[], poly_deg=4):
        self.poly_deg = poly_deg
        
        # Guess is either user input or np.ones with length of degree
        if len(init_guess) != 0:
            self.init_guess = init_guess
        else:
            self.init_guess = np.ones(self.poly_deg+1)
        
        if function_type == 'poly':
            self.func = self.arbitrary_poly
        else:
            self.func = self.arbitrary_poly

    def change_degree(self, new_degree):
        """Change polynomial degree
        
        Function to change degree of the fitting polynomial

        Args:
            new_degree (int): the specified degree of polynomial
        """

        self.poly_deg = new_degree
        # update the initial guesses as well to match the degree
        self.init_guess = np.ones(self.poly_deg+1)

    @staticmethod
    def arbitrary_poly(x, *params):
        """Make a polynomial function

        Function called by minimization routine to create polynomial

        Args:
            x (array): array of x values to compute poly model
            params (array): array of polynomial indices

        Returns: 
            The polynomial model
        """

        return sum([p*(x**i) for i, p in enumerate(params)])
        
class Fit(object):
    """Class to perform a fit

    Fit the data with a specified model

    Args:
        Data_object (class): a data object
        Model_object (class): a model object
        
    """

    def __init__(self, Data_object, Model_object):
        self.data = Data_object
        self.model = Model_object

        # Run a fit each time the class is instantiated
        self.y_model, self.popt, self.x_model = self.run_fit()
        

    def run_fit(self):
        """Run fit

        Performs a fit to the data with a minimization routine, currently uses scipy curve_fit


        Returns: 
            y_model (array): The best fit model
            popt (array): The best fit parameter values for the fitting function
            x_model (array): The x array of the model

        """

        popt, pcov = curve_fit(self.model.func, self.data.x[self.data.mask],
                             self.data.y[self.data.mask], sigma=self.data.yerr[self.data.mask],
                            p0=self.model.init_guess)

        # plot best fit model over finer x spacing
        x_model = np.linspace(np.min(self.data.x), np.max(self.data.x), 10*len(self.data.x))
        y_model = self.model.func(x_model, *popt)

        return y_model, popt, x_model

