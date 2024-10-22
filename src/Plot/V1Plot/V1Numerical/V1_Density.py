#!/usr/bin/env python3

# General libraries
import numpy as np
import matplotlib.pyplot      as plt
import matplotlib.ticker      as ticker
from matplotlib.colors import LinearSegmentedColormap

from scipy import stats

# Import the auxiliary libraries
import lib.utils         as my_utils_tools

# Import the main libraries
from ...Plot     import Plot
from ..V1Plot    import V1Plot
from ....Seagull import Seagull

class Density_plot(V1Plot):

    # Import the class methods
    from .methods.setters_getters import (set_data_x)

    # Default constructor
    def __init__(self, data = None, numerical_column_index:int = None, folder_path = None,  # Rearranged parameters for easy use
                 column:str = None,                                                         # Alias for numerical_column_index
                 extra_info:bool = True, show_points:bool = True, bandwidth = 0.5,          # Density plot parameters
                 **kwargs):                                                                 # Other parameters

        # -----------------------------------------
        # Data related
        # -----------------------------------------
        invalid_data_index = True # Assume the index is invalid until proven otherwise
        self.data_x = None
        self.data_name   = None
        self.data_name_x = None     
        self.data_name_y = None

        # -----------------------------------------
        # Styler related
        # -----------------------------------------
        # Python is shit man, it let you init variable whetever, that's why C++ is best and you won't have bugs related to that
        # it took me forever to find this bug and move this section to the start

        # Labels related
        self.extra_info     = extra_info  # If True, it will show the mean and percentiles
        self.cloudpoints    = show_points # If True, it will show the jitter cloudpoints

        # Style related
        self.line_thickness    = 2
        self.color_line        = 'salmon'
        self.color_fill_start  = 'lightcoral'
        self.color_fill_end    = None
        self.color_alpha_start = 0.5
        self.color_alpha_end   = 0.5
        self.color_alpha_stop  = 0.5
        
        # -----------------------------------------
        # Do the parent constructor first
        # -----------------------------------------
        super().__init__(folder_path = folder_path, **kwargs)  # Pass common parameters to the parent constructor

        # -----------------------------------------
        # Update the parent class attributes second
        # -----------------------------------------

        # Default figure size, can and will be updated automatically later
        # but for a density plot this seems a good proportion

        if(self.manual_size == False):
            self.figure_width  = 10 
            self.figure_height = 5

        # Plot type
        self.type = "Density Plot"

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------

        # Plot format related
        self.bandwidth      = bandwidth   # Smaller values give more detail

        # Solve the column alias
        # We don't have the index
        if(numerical_column_index == None):
            # But we have the column alias
            if(column != None):
                numerical_column_index = column
                invalid_data_index     = False
            # We don't have anything
            # This is allowed, the user might change it later, but can't init the plot with data now if that is his idea
        # We have the index
        else:

            # If we have an index, we can use it
            invalid_data_index = False

            # But we also have the column?
            # Ignore the column
            if(column != None):
                print()
                print("WARNING!: Both column ("+ str(column) +") and numerical_column_index ("+ str(numerical_column_index) +") were given.")
                print("          numerical_column_index will be used.")
                print()

            # If we don't have the column
            # That's also fine, we can use the index

        # If we have a data object, use that
        if(data != None):

            # If we have a Seagull object, try to init the data from it
            if(type(data).__name__ == 'Seagull'):

                # If the index is valid, you can init it
                if(invalid_data_index == False):

                    # Check if the numerical is a string and transform it into an integer
                    # -- If it is a string we will assume the user mean the column name
                    #    If the user meant the column index as a string, then it will interpret
                    #    it as a column name. If it doesn't exist will rise an error. But
                    #    if it does, it will use it and be confusing until the user realizes.
                    if(type(numerical_column_index) == str):

                        index_candidate = data.get_column_index(numerical_column_index)
                        if(index_candidate < 0):

                            print()
                            print("ERROR!: The given column: " + str(numerical_column_index) + " is not valid.")
                            print("        I tried to find the name and couldn't find an index for that column.")
                            print()
                            print("        Current columns are:.")
                            print()
                            print("        " + str(data.getColumnsNames()))
                            print()
                            print("        The plot haven't changed.")
                            print()

                        else:
                            numerical_column_index =  data.get_column_index(numerical_column_index)

                    # If the filename is not set, set it automatically
                    if(self.filename == None):
                        self.init_from_seagull(data, numerical_column_index, autoupdate_labels = False, autoupdate_filename = True)
                    else:
                        self.init_from_seagull(data, numerical_column_index, autoupdate_labels = False, autoupdate_filename = False)
                    
                    self.data_name_y = "Density"

                # If the seagull was valid, but neither the index or the column, rise an error
                else:
                    print()
                    print("ERROR!: The given column: " + str(numerical_column_index) + " is not valid.")
                    print("        The plot haven't changed.")
                    print()

            # If we don't have seagull, try to init the data from np.array, panda, or wahtever
            else:
                self.data_name   = "Given Data"
                self.data_name_x = "X"      
                self.data_name_y = "Density"

                # Update filename, if none was given
                if(self.filename == None): self.filename = "Density_Plot"

        # Otherwise, use random data
        else:

            self.data_x = np.sort(np.random.rand(100)) # Initialize a random array
            self.data_x = (2 * self.data_x) - 1        # Scale between -1 and 1
            self.data_name   = "Random Data"
            self.data_name_x = "X"      
            self.data_name_y = "Density"

            # Update filename, if none was given
            if(self.filename == None): self.filename = "Density_Plot"

        # Update the titles if required
        self.automatic_titles()


        # -----------------------------------------
        # Update the figure
        # -----------------------------------------
        self.automatic_size()
        self.update_figure()


    # Initialize the plot from a Seagull instance
    def init_from_seagull(self, seagull_instance:Seagull, numerical_column_index:int, autoupdate_labels = True, autoupdate_filename = True):

        target_column_index = 0
        target_column_name  = ""

        # Check if the index is integer or string.
        # If string, transform it into an integer
        if(type(numerical_column_index) == str):
            target_column_name  = numerical_column_index
            target_column_index = seagull_instance.getColumnIndex(numerical_column_index)
        else:
            target_column_name  = seagull_instance.get_column_name(numerical_column_index)
            target_column_index = numerical_column_index

        # Check if the data is numerical
        if(not seagull_instance.isNumerical(target_column_index)):

            # Error message
            print("ERROR!: The given column: " + str(numerical_column_index) + " is not numerical.")
            print()
            print("        I need it to be either integer or float of any bit size (16, 32...).")
            print("        The plot haven't changed.")
            print()

        else:

            # Get the data
            self.data_x      = np.sort(seagull_instance.get_column_values(target_column_index))
            self.data_name   = seagull_instance.getName()
            self.data_name_x = target_column_name

            # Update if required
            # ---- Filename
            if(autoupdate_filename):
                self.filename = self.data_name + "_"+str(self.data_name_x)+"_Density_Plot"
                self.filename = my_utils_tools.clean_weird_characters(self.filename)

            # ---- Labels
            if(autoupdate_labels): self.automatic_titles()

            # Update the figure
            self.update_figure()

    # Automic figure size
    def automatic_size(self):

        # Automatic size is the same as the default size
        # 1D plot don't need to adjust the size as there is only one known source of information
        self.figure_width  = 10 
        self.figure_height = 5

    # Set the titles automatically based on the data
    # and if the user didn't set them manually before
    def automatic_titles(self):

        self.label_title    = "Density Plot for "  + self.data_name_x + " in " + self.data_name
        self.label_subtitle = "Kernel estimator: " + str(self.bandwidth)
        self.label_x_axys   = self.data_name_x
        self.label_y_axys   = self.data_name_y

    # Switch showing extra data or not
    def show_extra_info(self, show = True):
        self.extra_info = show

    # Set the style of the plot (evertything related to colors)
    def style(self, line_thickness    = None, color_line      = None,
                    color_fill_start  = None, color_fill_end  = None,
                    color_alpha_start = None, color_alpha_end = None,
                    color_alpha_stop  = None):

        # Values set to None doesn't change and keep whatever was set before
        if(line_thickness    != None): self.line_thickness    = line_thickness
        if(color_line        != None): self.color_line        = color_line
        if(color_fill_start  != None): self.color_fill_start  = color_fill_start
        if(color_fill_end    != None): self.color_fill_end    = color_fill_end
        if(color_alpha_start != None): self.color_alpha_start = color_alpha_start
        if(color_alpha_end   != None): self.color_alpha_end   = color_alpha_end
        if(color_alpha_stop  != None): self.color_alpha_stop  = color_alpha_stop
    
    # Update the figure based on the data we have in the object
    def update_figure(self):
        """
        Creates a density plot using:
            1D NumPy float array for the numbers.
        """

        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(self.figure_width, self.figure_height))

        # Create the density data
        # The gaussian estimator can be swapped for other estimators easily
        density      = stats.kde.gaussian_kde(self.data_x, bw_method = self.bandwidth)
        density_data = density(self.data_x)

        # Calculate percentiles and mean
        percentiles = np.percentile(self.data_x, [5, 25, 50, 75, 95])
        mean_value  = np.mean(self.data_x)

        # Density Plot
        ax.plot(self.data_x, density_data, color = self.color_line, linewidth = self.line_thickness)


        # When there is a lot of data the density can be very small 1e-5-ish or less
        # In those cases the density numbers are ugly in the plot if they are too long 0.0000000000001 for example
        # If you try to find the minimum of the data, and keep consistent exponential, then the leading number can be too high
        # if the difference is too big, 1e-5 and 1000e-5 for example.
        # I found a good automatic solution, which is find the median of the y-axis values and keep that one as exponent reference
        # If the user still don't like it, then he can change it manually later using the plot object figure and axis.
        #
        # Set the y-axis format to scientific if the density is too low
        percentiles_y_axis = np.percentile(density_data, [5, 10, 15, 50])
        order_of_magnitude = np.floor(np.log10(abs(percentiles_y_axis[3])))
        if(min(density_data) < 0.0001):
            #ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.0e}'))

            # Set the y-axis format to scientific notation with a consistent exponent
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(
                lambda x, _: f'{x / 10**order_of_magnitude:.0f}e{int(order_of_magnitude)}'
            ))

 

        # Fill under the line
        #
        # No color: (do nothing)
        # If we have starting color...
        if(self.color_fill_start != None):

            # Solid color with constants transparency
            if(self.color_fill_end == None):
                ax.fill_between(self.data_x, density_data, color = self.color_fill_start, alpha = self.color_alpha_start)

            # Gradient color with variable transparency
            else:
                num_layers  = 50
                start_color = self.color_fill_start
                end_color   = self.color_fill_end
                custom_cmap = LinearSegmentedColormap.from_list("custom_gradient", [start_color, end_color])
                colors = custom_cmap(np.linspace(0, 1, num_layers))

                # Create a matrix where each row is density_data
                density_matrix = np.tile(density_data, (num_layers, 1))
                max_density    = np.max(density_data)
                displacement   = max_density / num_layers

                for i in range(1, num_layers):
                    density_matrix[i] = np.maximum(density_matrix[i] - i * displacement, 0)

                for i, current_color in enumerate(colors):

                    if (i / num_layers <= self.color_alpha_stop):
                        current_alpha = self.color_alpha_start + (self.color_alpha_end - self.color_alpha_start) * (i / (num_layers * self.color_alpha_stop))
                    else:
                        current_alpha = self.color_alpha_end

                    #ax.fill_between(self.data, density_data, color = current_color, alpha = current_alpha, zorder = i)

                    if(i < (num_layers - 1)):

                        ax.fill_between(self.data_x, density_matrix[i], density_matrix[i + 1],
                                        color = current_color, alpha = current_alpha, # zorder = i,
                                        linewidth = 0, edgecolor = None )


                # Add auxiliary grid line
        
        
        
        
                # Add vertical lines for percentiles
        
        # If extra info is requested add it
        if(self.extra_info):

            # The title will need extra space
            # plt.subplots_adjust(top=0.85)  # Adjust the top spacing (this is above the title, save for later)

            #percentile_labels = [5, 25, 50, 75, 95]
            #for percentile, label in zip(percentiles, percentile_labels):
            #    ax.axvline(x = percentile, color = self.color_line, linestyle = '--', linewidth=1)
            #    ax.text(percentile, max(density_data) * 1.06, f'{label}%', horizontalalignment = 'center')
                


            # Calculate percentiles
            percentiles = np.percentile(self.data_x, [95, 75, 50, 25, 5])  # Reversed order
            percentile_labels = [95, 75, 50, 25, 5]  # Corresponding labels in reversed order

            # Variables to track the previous percentile position
            previous_percentile = None

            for percentile, label in zip(percentiles, percentile_labels):

                # Draw the vertical line
                ax.axvline(x = percentile, color = self.color_line, linestyle = '--', linewidth=1)

                if previous_percentile is not None and (previous_percentile - percentile) / (max(self.data_x) - min(self.data_x)) < 0.05:
                    # Skip drawing the label if the current percentile is less than 5% of the data range closer to the previous one
                    continue

                # Add text label
                ax.text(percentile, max(density_data) * 1.06, " " + str(label) + "%", horizontalalignment = 'center')
    
                # Update the previous percentile
                previous_percentile = percentile


            # Add a vertical line for the mean
            ax.axvline(x = mean_value, color = self.color_line, linestyle='-', linewidth = 2)

        
        # If the cloudpoint is requested, add it
        if(self.cloudpoints):

     

            # Calculate the maximum density to determine the jitter range
            max_density = max(density_data)
            max_jitter = 0.1 * max_density  # 10% of the maximum density

            # Introduce some random jitter to the y-values within the range [0, max_jitter]
            y_jitter = np.random.uniform(low=0, high=max_jitter, size=len(self.data_x))

            # Plot the jittered points
            ax.scatter(self.data_x, y_jitter, color=self.color_line, alpha=0.5)  # Use a contrasting color for visibility


        # ---------------------------------------------------------------------
        # Plot theme:
        # ---------------------------------------------------------------------

        # Apply the theme for the plot
        ax.grid(color ='grey',
                linestyle ='-.', linewidth = 0.5,
                alpha = 0.2)
        

        # Add the common plots labels

        # Add Plot Title and subtitle
        total_padding = 0
        if(self.extra_info):           total_padding += 15
        if(self.label_subtitle!=None): total_padding += 15
        
        ax.set_title(self.label_title, loc = 'left', pad = total_padding)
        
        # Adding a subtitle using text
        if(self.label_subtitle!=None):
            ax.text(0, 1.1, self.label_subtitle, transform = ax.transAxes, ha = 'left', va = 'top', fontsize = 10, color = 'gray')


        # Update and add Plot X and Y axys
        self.label_x_axys   = self.data_name_x
        self.label_y_axys   = self.data_name_y

        ax.set_xlabel(self.label_x_axys)
        ax.set_ylabel(self.label_y_axys)

        # Uodate the figure internatl object
        self.figure = fig
        self.axes   = ax