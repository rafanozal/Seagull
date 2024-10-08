#!/usr/bin/env python3

# General libraries
import numpy as np
import matplotlib.pyplot      as plt
import matplotlib.patheffects as PathEffects
from matplotlib.colors import LinearSegmentedColormap
import string

from scipy import stats

# Import the auxiliary libraries
import lib.color_manager as mytools

# Import the main libraries
from ...Plot     import Plot
from ....Seagull import Seagull


class Density_plot(Plot):

    # Default constructor
    def __init__(self, folder_path = None, filename = None):

        # -----------------------------------------
        # Do the parent constructor first
        # -----------------------------------------
        super().__init__(folder_path, filename)

        # -----------------------------------------
        # Update the parent class attributes second
        # -----------------------------------------

        # Default figure size, can and will be updated automatically later
        self.figure_width  = 10 
        self.figure_height = 5

        # Plot type
        self.type = "Density Plot"

        # Update filename, if none was given, use the HorizontalBarplot as default
        if(self.filename == None):
            self.filename = "DensityPlot"

        # Figure stays the same, to be updated later

        # Plot labels stay the same, to be updated later

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------

        # Data related
        self.data = np.sort(np.random.rand(100)) # Initialize a random array
        self.data = (2 * self.data) - 1          # Scale between -1 and 1
        self.data_name   = None
        self.data_name_x = "X"      
        self.data_name_y = "Density"

        # Labels related
        self.extra_info     = False # If True, it will show the mean and percentiles

        # Plot format related
        self.bandwidth      = 0.5   # Smaller values give more detail
        
        # Style related
        self.line_thickness    = 2
        self.color_line        = 'salmon'
        self.color_fill_start  = 'lightcoral'
        self.color_fill_end    = None
        self.color_alpha_start = 0.5
        self.color_alpha_end   = 0.5
        self.color_alpha_stop  = 0.5

        # Common text related

        # -----------------------------------------
        # Update the figure
        # -----------------------------------------
        self.automatic_size()
        self.update_figure()

    # Initialize the plot from a Seagull instance
    def init_from_seagull(self, seagull_instance:Seagull, numerical_column_index:int):

        target_column_index = 0
        target_column_name  = ""

        # Check if the index is integer or string.
        # If string, transform it into an integer
        if(type(numerical_column_index) == str):
            target_column_name  = numerical_column_index
            target_column_index = seagull_instance.getColumnIndex(numerical_column_index)
        else:
            target_column_name  = seagull_instance.getColumnName(numerical_column_index)
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
            self.data        = np.sort(seagull_instance.getValues(target_column_index))
            self.data_name   = seagull_instance.getName()
            self.data_name_x = target_column_name

            # Update the figure
            self.automatic_titles()
            self.update_figure()


        # Update the figure
        self.automatic_titles()
        self.update_figure()

    # Automic figure size
    def automatic_size(self):

        # Automatic size is the same as the default size
        # 1D plot don't need to adjust the size as there is only one known source of information
        self.figure_width  = 10 
        self.figure_height = 5

    # Set the titles automatically based on the data
    def automatic_titles(self):
        self.label_title    = "Density Plot"
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
        density      = stats.kde.gaussian_kde(self.data, bw_method = self.bandwidth)
        density_data = density(self.data)

        # Calculate percentiles and mean
        percentiles = np.percentile(self.data, [5, 25, 50, 75, 95])
        mean_value  = np.mean(self.data)

        # Density Plot
        ax.plot(self.data, density_data, color = self.color_line, linewidth = self.line_thickness)

        # Fill under the line
        #
        # No color: (do nothing)
        if(self.color_fill_start != None):

            # Solid color with constants transparency
            if(self.color_fill_end == None):
                ax.fill_between(self.data, density_data, color = self.color_fill_start, alpha = self.color_alpha_start)

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

                        ax.fill_between(self.data, density_matrix[i], density_matrix[i + 1],
                                        color = current_color, alpha = current_alpha, zorder = i,
                                        linewidth = 0, edgecolor = None )


                # Add auxiliary grid line
        
        
        
        
                # Add vertical lines for percentiles
        
        # If extra info is requested add it
        if(self.extra_info):

            # The title will need extra space
            # plt.subplots_adjust(top=0.85)  # Adjust the top spacing (this is above the title, save for later)

            percentile_labels = [5, 25, 50, 75, 95]
            for percentile, label in zip(percentiles, percentile_labels):
                ax.axvline(x=percentile, color=self.color_line, linestyle='--', linewidth=1)
                ax.text(percentile, max(density_data) * 1.06, f'{label}%', horizontalalignment = 'center')

            # Add a vertical line for the mean
            ax.axvline(x=mean_value, color=self.color_line, linestyle='-', linewidth=2)

        
        # Apply the theme for the plot
        ax.grid(color ='grey',
                linestyle ='-.', linewidth = 0.5,
                alpha = 0.2)
        

        # Add the common plots labels

        # Add Plot Title
        total_padding = 0
        if(self.extra_info):           total_padding += 15
        if(self.label_subtitle!=None): total_padding += 15
        
        ax.set_title(self.label_title, loc = 'left', pad = total_padding)
        
        # Adding a subtitle using text
        if(self.label_subtitle!=None):
            ax.text(0, 1.1, self.label_subtitle, transform = ax.transAxes, ha = 'left', va = 'top', fontsize = 10, color = 'gray')


        # Add Plot X and Y axys
        ax.set_xlabel(self.label_x_axys)
        ax.set_ylabel(self.label_y_axys)

        # Uodate the figure internatl object
        self.figure = fig
        self.axes   = ax