import numpy as np
from scipy.optimize import curve_fit

class Data(object):

    def __init__(self, x, y, yerr ):
        self.x = x
        self.y = y
        self.yerr = yerr

        self.mask = np.ones_like(x).astype(bool)


class Model(object):

    def __init__(self, function_type, init_guess, poly_deg=4):
        self.init_guess = init_guess
        if function_type == 'poly':
            self.func = self.arbitrary_poly
        else:
            self.func = self.arbitrary_poly

    @staticmethod
    def arbitrary_poly(x, *params):
        # print(x)
        # print(params)
        return sum([p*(x**i) for i, p in enumerate(params)])
        
class Fit(object):

    def __init__(self, Data_object, Model_object):
        self.data = Data_object
        self.model = Model_object

        self.y_model, self.popt, self.x_model = self.run_fit()
        

    def run_fit(self):

        # call scipy for fit
        # [self.data.mask]
        popt, pcov = curve_fit(self.model.func, self.data.x,
                             self.data.y, sigma=self.data.yerr,
                            p0=self.model.init_guess)

        # get best fit model
        x_model = np.linspace(np.min(self.data.x), np.max(self.data.x), 10*len(self.data.x))
        y_model = self.model.func(x_model, *popt)

        return y_model, popt, x_model


    # def compute_chi2(self, Data_object):
        
# # Quick example
# x_data = np.linspace(1,10,10) 
# y_data = x_data**2 * 5 + np.random.rand(10)

# # print(y_data.shape, x_data.shape)

# y_err = np.ones_like(x_data) * 0.1

# guess = np.zeros(4)
# d = Data(x_data,y_data,y_err)
# m = Model('poly', guess)

# fit_obj = Fit(d, m)

# print(fit_obj.y_model)
# print(fit_obj.popt)