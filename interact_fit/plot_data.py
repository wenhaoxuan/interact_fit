import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from data_model import Data, Model, Fit


class MakePlot(object):
    def __init__(self, Data_Object, Model_Object, Fit_Object):
        # Read in the data
        self.data = Data_Object
        
        # Read in the model 
        self.Model = Model_Object

        # Read in the fits from the model
        self.fit = Fit_Object

        self.setup_plot()
        self.plot_data()
        plt.show()

    def setup_plot(self):
        """
        Sets the framework for the matplotlib plot          
        """
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = plt.axes([0.05, 0.3, 0.9, 0.65])   # Set axis dimensions here

        def onclick(event):
            """
            Updates the self.click_x and self.click_y variables upon click, then runs the update_mask() method
            """
            self.click_x, self.click_y = event.xdata, event.ydata
            print(f'You clicked x = {self.click_x}, y = {self.click_y}')
            
            # Check if the click was inside of the plot
            x_lim = self.ax.get_xlim()
            y_lim = self.ax.get_ylim()
            if self.click_x != None and self.click_y != None:
                if event.inaxes ==self.ax: 
                        self.update_mask()
                        self.update_fit()
            return

        self.ax_change_degree = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor='coral')

        self.poly_slider = Slider(
            ax=self.ax_change_degree,
            label='Polynomial Degree',
            valmin=0,
            valmax=len(self.data.x[self.data.mask]),
            valinit=self.Model.poly_deg,
            valstep=1
        )

        def poly_slider_update(new_deg):
            self.Model.change_degree(new_deg)
            self.update_fit()


        # Updates to plot when clicked
        cid = self.fig.canvas.mpl_connect('button_press_event', onclick)
        self.poly_slider.on_changed(poly_slider_update)

    def plot_data(self):
        """
        Plots the data and the model         
        """
        self.ax.cla()
        self.ax.plot(self.data.x, self.data.y, color='black', marker='o', ls='None')
        self.ax.plot(self.data.x[~self.data.mask], self.data.y[~self.data.mask], color='red', marker='x', ms=10, lw=0.1, ls='None') 
        self.ax.plot(self.fit.x_model, self.fit.y_model, color='orange', marker='None', ls='-')
        
        # Update slider length
        self.poly_slider.valmax = len(self.data.x[self.data.mask])-1
        
        plt.draw()
          

    def update_mask(self):
        """
        Updates the mask by removing the point closest to where the user clicked        
        """
        # Compute the pythagorean distance between the click and each point
        x_lim = self.ax.get_xlim()
        y_lim = self.ax.get_ylim()
        
        # Needed to scale to account for possibly different lengths of x and y axis
        x_dist_scaled = (self.data.x - self.click_x)/np.abs(x_lim[1]-x_lim[0])
        y_dist_scaled = (self.data.y - self.click_y)/np.abs(y_lim[1]-y_lim[0])
        distances = np.sqrt(x_dist_scaled**2 +
                            y_dist_scaled**2)
        # Find the minimum index, should correspond to closest point to where clicked
        min_idx = np.argmin(distances)
        print(f'Nearest point is {(self.data.x[min_idx], self.data.y[min_idx])}')

        #update here
        self.data.mask[min_idx] = ~self.data.mask[min_idx]

        if len(self.data.x[self.data.mask]) < self.Model.poly_deg+1:
            self.data.mask[min_idx] = ~self.data.mask[min_idx]
        
        return

    def update_fit(self):
        self.fit = Fit(self.data, self.Model)
        self.plot_data()


        # plt.close('all')
        # MakePlot(New_Data, self.Model, New_Fit)
        


# Quick example
# x_data = np.linspace(1,10,10) 
# y_data = x_data**2 * 5 + np.random.rand(10)
# y_data = x_data + np.random.rand(10)

# # print(y_data.shape, x_data.shape)

# y_err = np.ones_like(x_data) * 0.1

# guess = np.zeros(4)
# d = Data(x_data,y_data,y_err)
# m = Model('poly', guess)

# fit_obj = Fit(d, m)

# print(fit_obj.y_model)
# print(fit_obj.popt)

# MakePlot(d, m, fit_obj)