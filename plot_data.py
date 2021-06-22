import numpy as np
import matplotlib.pyplot as plt


class MakePlot(object):
    def __init__(self, Data_Object, Model_Object):
        # # Read in the data
        # self.x = Data_Object.x
        # self.y = Data_Object.y
        # self.yerr = Data_Object.yerr

        # # Read in the fits from the model
        # self.fit = Model_Object.fit
        self.x = np.arange(10)
        self.y = np.array([1, -3, 5, 6, -10, 5, 3, 8, 9, 0])
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
            self.update_mask()
            return
        cid = self.fig.canvas.mpl_connect('button_press_event', onclick)

    def plot_data(self):
        """
        Plots the data and the model         
        """
        self.ax.plot(self.x, self.y, color='black', marker='o', ls='None')

    def update_mask(self):
        """
        Updates the mask by removing the point closest to where the user clicked        
        """
        # Compute the pythagorean distance between the click and each point
        x_lim = self.ax.get_xlim()
        y_lim = self.ax.get_ylim()
        
        # Needed to scale to account for possibly different lengths of x and y axis
        x_dist_scaled = (self.x - self.click_x)/np.abs(x_lim[1]-x_lim[0])
        y_dist_scaled = (self.y - self.click_y)/np.abs(y_lim[1]-y_lim[0])
        distances = np.sqrt(x_dist_scaled**2 +
                            y_dist_scaled**2)
        # Find the minimum index, should correspond to closest point to where clicked
        min_idx = np.argmin(distances)
        print(f'Nearest point is {(self.x[min_idx], self.y[min_idx])}')

        # UPDATE THE MASK HERE WITH SOMETHING LIKE
        # .mask[min_idx] = 0


MakePlot(1, 1)
