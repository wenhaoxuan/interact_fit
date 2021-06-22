import numpy as np
from scipy.optimize import curve_fit

class Data(object):

    def __init__(self, x, y, yerr ):
        self.x = x
        self.y = y
        self.yerr = yerr

        self.mask = np.ones_like(x)


class Model(object):

    def __init__(self, Data_object, function_type, init_guess, poly_deg=4):
        self.init_guess = init_guess
        self.data = Data_object
        
        if function_type == 'poly':
            self.func = self.arbitrary_poly
        
        else:
            self.func = self.arbitrary_poly
        


    def run_fit(self):

        # call scipy for fit
        popt, pcov = curve_fit(self.func, self.data.x, self.data.y, sigma=self.data.yerr,
                            p0=self.init_guess)

        print(popt, pcov)

    @staticmethod
    def arbitrary_poly(x, *params):
        return sum([p*(x**i) for i, p in enumerate(params)])

    # def compute_chi2(self, Data_object):
        
# Quick example
# x_data = np.linspace(1,10,10) 
# y_data = x_data**2 * 5 + np.random.rand(10)

# print(y_data.shape, x_data.shape)

# y_err = np.ones_like(x_data) * 0.1

# d = Data(x_data,y_data,y_err)

# guess = np.ones(4)
# m = Model(d, 'poly', guess)

# m.run_fit()