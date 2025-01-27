#!/usr/bin/env python3

# General libraries
import numpy as np
import matplotlib.pyplot      as plt
import matplotlib.ticker      as ticker

from scipy import stats

# Import the auxiliary libraries
import lib.color_manager as color_manager

# Import the main libraries
from ..V2_Num_Cat import V2_Num_Cat

class Distributions_plot(V2_Num_Cat):

    # Import the class methods
    #from .methods.setters_getters import (set_data_x_list)

    # Default constructor
    def __init__(self, data  = None, numerical_column_index = None, categorical_column_index = None,
                 folder_path = None,                                                                 # Rearranged parameters for easy use
                 extra_info:bool = True, show_points:bool = True, bandwidth = 0.5,                   # Density plot parameters
                 color_list = None, line_thickness_list = None, color_alpha_list = None,             # Style parameters
                 **kwargs):                                                                          # Other parameters

        print("AA Current Filename: ", folder_path)

        # -----------------------------------------
        # Do the parent constructor first
        # -----------------------------------------
        super().__init__(data                     = data,
                         numerical_column_index   = numerical_column_index,
                         categorical_column_index = categorical_column_index,
                         folder_path              = folder_path,
                         **kwargs) # Pass common parameters to the parent constructor

        self.type        = "Multivariate Density Plot"
        self.data_name_y = "Density"
        
        print("DENSITY PLOT CONSTRUCTOR")
        print()
        print("Plot filename: ", self.filename)
        print("Plot folder path: ", self.folder_path)
        print()

        # -----------------------------------------
        # Class attributes
        # -----------------------------------------
        
        # Python is shit man, it let you init variable whetever, that's why C++ is best and you won't have bugs related to that
        # it took me forever to find this bug and move this section to the start

        # Labels related
        self.extra_info     = extra_info  # If True, it will show the mean and percentiles
        self.cloudpoints    = show_points # If True, it will show the jitter cloudpoints

        # Style related (init to default if None is given)
        self.line_thickness_list = line_thickness_list
        self.color_line_list     = color_list
        self.color_alpha_list    = color_alpha_list 
        self.set_style()                                     # If any of the style values is none, this take care of setting it to something reasonable

        # Density related
        self.bandwidth = bandwidth   # Smaller values give more detail

        # Update everything
        self.automatic_titles()
        self.automatic_size()
        self.automatic_filename()
        self.update_figure()

        print("CC Current Filename: ", self.folder_path)

    # Automic figure size
    def automatic_size(self):

        # Automatic size is the same as the default size
        # The density plots don't scale with more categories or data
        self.figure_width  = 10 
        self.figure_height = 5

    # Set the titles automatically based on the data
    # and if the user didn't set them manually before
    def automatic_titles(self):

        self.label_title    = "Density Plot for "  + self.data_numerical_name + " and " + self.data_categorical_name + " in " + self.data_name
        self.label_subtitle = "Kernel estimator: " + str(self.bandwidth)
        self.label_x_axys   = ""
        self.label_y_axys   = self.data_name_y

    # Set the filename automatically for this type of plot
    def automatic_filename(self):

        # Init the strings for making the filename
        string_category = self.data_categorical_index
        string_numeric  = self.data_numerical_index
        string_data     = self.data_name

        # Correct their values if needed
        # < 0 means the data was init randomly, hence no index
        string_category = None if string_category < 0 else str(string_category)
        string_numeric  = None if string_numeric  < 0 else str(string_numeric)


        # Put the strings together
        # If the strings are None, they won't be added to the filename

        join_indexes     = string_data
        string_indexes   = [string_category, string_numeric, string_data]
        filtered_indexes = [s for s in string_indexes if s is not None]
        if len(filtered_indexes) > 1:
            join_indexes = '_'.join(filtered_indexes)

        # Set the final filename
        self.filename   = "Multidensity_Plot_" + join_indexes


    # Switch showing extra data or not
    def show_extra_info(self, show = True):
        self.extra_info = show

    # Set the style of the plot (evertything related to colors)
    # If set_defaults = True, it will assign None values to default
    # If set_defaults = False, it will keep the previous values
    def set_style(self, color_list = None, line_thickness_list = None, color_alpha_list = None, set_defaults = False):
 
        # If the user gave a list of colors
        if(color_list != None):
            
            # If the user gave a list of colors
            if(type(color_list) == list):
                
                # Check that the list is the same length as the data
                if(len(color_list) != self.data_length):
                    print()
                    print("WARNING!: The color list you gave me is not the same length as the data.")
                    print("          I will use the default colors instead.")
                    print()
                    
                    self.color_list = color_manager.get_qualitative_colors(self.data_length)
            
                # If everything is correct, use that color list
                else:
                    self.color_list = color_list

            # If the user gave a single color
            # We will use the same color for all the data
            # (This would be quite ugly though, as all the lines will have the same color; WEIRD!)
            else:
                self.color_list = [color_list] * self.data_length            

        # Otherwise, init to default
        else:
            if(set_defaults or self.color_line_list == None): self.color_line_list = color_manager.get_qualitative_colors(self.data_length)
        

            
        # If the user gave a list of thickness
        if(line_thickness_list != None):
                
            # If the user gave a list of thickness
            if(type(line_thickness_list) == list):
                
                # Check that the list is the same length as the data
                if(len(line_thickness_list) != self.data_length):
                    print()
                    print("WARNING!: The line thickness list you gave me is not the same length as the data.")
                    print("          I will use the default thickness instead.")
                    print()
                    
                    self.line_thickness_list = [2] * self.data_length
            
                # If everything is correct, use that thickness list
                else:
                    self.line_thickness_list = line_thickness_list

            # If the user gave a single thickness
            # We will use the same thickness for all the data
            else:
                self.line_thickness_list = [line_thickness_list] * self.data_length
        
        # Otherwise, init to default
        else:
            if(set_defaults or self.line_thickness_list == None): self.line_thickness_list = [2] * self.data_length 
        


        # If the user gave a list of alphas
        if(color_alpha_list != None):
                    
            # If the user gave a list of alphas
            if(type(color_alpha_list) == list):
                
                # Check that the list is the same length as the data
                if(len(color_alpha_list) != self.data_length):
                    print()
                    print("WARNING!: The color alpha list you gave me is not the same length as the data.")
                    print("          I will use the default alpha instead.")
                    print()
                    
                    self.color_alpha_list = [0.5] * self.data_length
            
                # If everything is correct, use that alpha list
                else:
                    self.color_alpha_list = color_alpha_list

            # If the user gave a single alpha
            # We will use the same alpha for all the data
            else:
                self.color_alpha_list = [color_alpha_list] * self.data_length
        
        # Otherwise, init to default
        else:
            if(set_defaults or self.color_alpha_list == None): self.color_alpha_list = [0.5] * self.data_length        
        
    
    # Update the figure based on the data we have in the object
    def update_figure(self):

        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(self.figure_width, self.figure_height))

        # Create the density data
        # The gaussian estimator can be swapped for other estimators easily
        density_list = [None] * self.data_length
        density_data_list = [None] * self.data_length
        for i in range(self.data_length):
            density_list[i]      = stats.kde.gaussian_kde(self.data_numerical_list[i], bw_method = self.bandwidth)
            density_data_list[i] = density_list[i](self.data_numerical_list[i])

        # Calculate percentiles and mean
        percentiles_list         = [None] * self.data_length
        density_percentiles_list = [None] * self.data_length
        mean_value_list          = [None] * self.data_length
        for i in range(self.data_length):
            percentiles_list[i] = np.percentile(self.data_numerical_list[i], [5, 25, 50, 75, 95])
            mean_value_list[i]  = np.mean(self.data_numerical_list[i])

        for i in range(self.data_length):
            ax.plot(self.data_numerical_list[i], density_data_list[i],
                    color     = self.color_line_list[i],
                    linewidth = self.line_thickness_list[i],
                    alpha     = self.color_alpha_list[i],
                    label     = self.data_numerical_names[i])


        # When there is a lot of data the density can be very small 1e-5-ish or less
        # In those cases the density numbers are ugly in the plot if they are too long 0.0000000000001 for example
        # If you try to find the minimum of the data, and keep consistent exponential, then the leading number can be too high
        # if the difference is too big, 1e-5 and 1000e-5 for example.
        # I found a good automatic solution, which is find the median of the y-axis values and keep that one as exponent reference
        # If the user still don't like it, then he can change it manually later using the plot object figure and axis.
        #
        # Set the y-axis format to scientific if the density is too low
        percentiles_y_axis_list = [None] * self.data_length
        order_of_magnitude_list = [None] * self.data_length
        for i in range(self.data_length):
            percentiles_y_axis_list[i] = np.percentile(density_data_list[i], [5, 10, 15, 50])
            order_of_magnitude_list[i] = np.floor(np.log10(abs(percentiles_y_axis_list[i][3])))

        # If all the density data is smaller than 0.0001, then we need to use scientific notation
        # Find the absolute minimum in each sublist
        absolute_minima = 999
        for i in range(self.data_length):

            # Find the minimum in the sublist
            absolute_minima = min(absolute_minima, min(density_data_list[i]))

        if(absolute_minima < 0.0001):
            # Find the bigger order of magnitude
            maximum_order = np.argmax(order_of_magnitude_list)
            # Set the y-axis format to scientific notation with a consistent exponent
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(
                lambda x, _: f'{x / 10**maximum_order:.0f}e{int(maximum_order)}'
            ))
        


        # If the cloudpoint is requested, add it
        if(self.cloudpoints):

            # Calculate the maximum density to determine the jitter range
            absolute_maximum = -1
            for i in range(self.data_length):

                # Find the minimum in the sublist
                absolute_maximum = max(absolute_maximum, max(density_data_list[i]))

            max_jitter = 0.1 * absolute_maximum  # 10% of the maximum density

            # Introduce the jitter for each data
            for i in range(self.data_length):

                min_info_range = 0 + max_jitter*i
                max_info_range = max_jitter*(i+1)

                y_jitter = np.random.uniform(low = min_info_range, high = max_info_range, size=len(self.data_numerical_list[i]))

                # Plot the jittered points
                ax.scatter(self.data_numerical_list[i], y_jitter, color=self.color_line_list[i], alpha=0.3)

                # Calculate percentiles

                for j in range(len(percentiles_list[i])):
                    #ax.axvline(x = percentiles[j], color = self.color_list[i], linestyle = '--', linewidth=1, alpha=0.5)
                    ax.plot([percentiles_list[i][j], percentiles_list[i][j]], [min_info_range, max_info_range], 
                            color=self.color_line_list[i], linestyle = '--',
                            linewidth=2, alpha=0.8)


                # Add a vertical line for the mean
                #ax.axvline(x = mean_value_list[i], color = self.color_list[i], linestyle='-', linewidth = 2, alpha=0.7)

                ax.plot([mean_value_list[i], mean_value_list[i]], [min_info_range, max_info_range], 
                        color=self.color_line_list[i], linestyle = '-',
                        linewidth=5, alpha=0.9)



        # ---------------------------------------------------------------------
        # Plot theme:
        # ---------------------------------------------------------------------

        # Apply the theme for the plot
        ax.grid(color ='grey',
                linestyle ='-.', linewidth = 0.5,
                alpha = 0.2)
        
        # ---------------------------------------------------------------------
        # Plot labels:
        # ---------------------------------------------------------------------

        # Display the legend
        legend = ax.legend(title = self.data_categorical_name, loc = 'upper right')
        legend._legend_box.align = "left"
        #legend.get_title().set_ha('left')  # 'ha' is short for horizontalalignment


        # Update and add Plot X and Y axys
        self.label_x_axys   = self.data_numerical_name
        self.label_y_axys   = self.data_name_y

        

        # Add Plot Title and subtitle
        total_padding = 0
        if(self.extra_info):           total_padding += 15
        if(self.label_subtitle!=None): total_padding += 15
        
        ax.set_title(self.label_title, loc = 'left', pad = total_padding)
        
        # Adding a subtitle using text
        if(self.label_subtitle!=None):
            ax.text(0, 1.1, self.label_subtitle, transform = ax.transAxes, ha = 'left', va = 'top', fontsize = 10, color = 'gray')

        ax.set_xlabel(self.label_x_axys)
        ax.set_ylabel(self.label_y_axys)

        # Uodate the figure internal object
        self.figure = fig
        self.axes   = ax