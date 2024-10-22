#!/usr/bin/env python3

# General libraries
import numpy as np
import matplotlib.pyplot      as plt
import matplotlib.ticker      as ticker
from matplotlib.colors import LinearSegmentedColormap

from scipy import stats

# Import the auxiliary libraries
import lib.color_manager as color_manager
import lib.utils         as my_utils_tools
import lib.solvers       as my_solvers

# Import the main libraries
from ...Plot      import Plot
from ..VN_Plot    import VN_Plot
from ....Seagull  import Seagull

# Constants
from src import constants

class Distributions_plot(VN_Plot):

    # Import the class methods
    #from .methods.setters_getters import (set_data_x_list)

    # Default constructor
    def __init__(self, data  = None, numerical_column_index_list = None, folder_path = None,  # Rearranged parameters for easy use
                 column_list = None,                                                          # Alias for numerical_column_index
                 extra_info:bool = True, show_points:bool = True, bandwidth = 0.5,            # Density plot parameters
                 color_list = None, line_thickness_list = None, color_alpha_list = None,      # Style parameters
                 **kwargs):                                                                   # Other parameters

        # -----------------------------------------
        # Data related
        # -----------------------------------------
        self.data_length      = 2
        self.data_x_list      = [None] * self.data_length
        self.data_name_x_list = [None] * self.data_length     
        self.data_name        = None
        self.data_name_y      = None

        # -----------------------------------------
        # Styler related
        # -----------------------------------------
        # Python is shit man, it let you init variable whetever, that's why C++ is best and you won't have bugs related to that
        # it took me forever to find this bug and move this section to the start

        # Labels related
        self.extra_info     = extra_info  # If True, it will show the mean and percentiles
        self.cloudpoints    = show_points # If True, it will show the jitter cloudpoints

        # Style related
        self.line_thickness_list = None
        self.color_line_list     = None
        self.color_alpha_list    = None 
        
        
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
        self.type = "Multivariate Density Plot"

        # -----------------------------------------
        # Start the actual constructor
        # -----------------------------------------
        
        # We need to figure out how much data slots we have.
        # We need at least one data slot to work
        # Ideally, the users give us a list, but it can work with only one index

        have_indexes = False
        have_columns = False

        #print(numerical_column_index_list)

        # If the user gave a list of indexes (ignore columns if both are given)
        if(numerical_column_index_list != None):
                
            have_indexes = True

            # Check that we have a list
            if(type(numerical_column_index_list) == list):

                # Check the length of the list
                self.data_length = len(numerical_column_index_list)

            # If the user gave a single index
            else:
                self.data_length = 1

        # If the user gave a list of columns
        elif(column_list != None):

            have_columns = True

            # Check that we have a list
            if(type(column_list) == list):

                # Check the length of the list
                self.data_length = len(column_list)

            # If the user gave a single index
            else:
                self.data_length = 1

        # If the user gave neither
        # We will init to random data with two slots
        else:
            self.data_length = 2

        #print(have_indexes)
        #print(have_columns)

        # Prepare the list where we solve the ambiguity
        solved_parameters_list = [None] * self.data_length
        if(have_indexes):
            for i in range(self.data_length):
                solved_parameters_list[i] = my_solvers.solve_source_data(data, numerical_column_index_list[i], None, constants.NUMERICAL_TYPES)
        elif(have_columns):
            for i in range(self.data_length):
                solved_parameters_list[i] = my_solvers.solve_source_data(data, None, column_list[i], constants.NUMERICAL_TYPES)
        else:
            for i in range(self.data_length):
                solved_parameters_list[i] = [None, -1, True]

        # Check that the solution is valid
        #
        #     - If a seagull or pandas, with index > 0, and the data is as expected
        #     - If numpy array and the data is as expected
        #
        # Otherwise default to random data
        valid_origin = False * self.data_length

        # Check that all origins are valid
        for i in range(self.data_length):

            if(not((solved_parameters_list[i][0] == "Seagull" and solved_parameters_list[i][1] > 0 and solved_parameters_list[i][2] == True) or \
                   (solved_parameters_list[i][0] == "Pandas"  and solved_parameters_list[i][1] > 0 and solved_parameters_list[i][2] == True))):
                
                # In this case, if the data is None, is not valid, but is not an error either
                if(solved_parameters_list[i][0] != None):

                    print()
                    print("WARNING!: The data you gave me in " + str(i) + " is not valid.")
                    print("          I will use random data instead.")

            else:
                valid_origin[i] = True 
        

        # If the user gave no data or unknown data, use random data
        if(solved_parameters_list[0][0] == "Uknown"):

            print()
            print("WARNING!: I don't understand the data you gave me.")
            print("          I will use random data instead.")
            print()

        # Regardless of the data, we need to aloc the lists for the data
        self.data_x_list      = [None] * self.data_length
        self.data_name_x_list = [None] * self.data_length

        if((solved_parameters_list[0][0]) == None or (False in valid_origin)):

            # Init the random data
            for i in range(self.data_length):
                self.data_x_list[i]       = np.sort(np.random.rand(100))   # Initialize a random array
                self.data_x_list[i]       = (2 * self.data_x_list[i]) - 1  # Scale between -1 and 1
                self.data_name_x_list[i]  = "Random " + str(i) + " Data"

            self.data_name_list = "Random Table"
            self.data_name_y    = "Density"    
            self.filename       = "Multidensity_Plot" 

        # If the user gave a Seagull object
        if(solved_parameters_list[0][0] == "Seagull"):

            for i in range(self.data_length):
                self.data_x_list[i]       = data.get_column_values(solved_parameters_list[i][1])
                self.data_name_x_list[i]  = data.get_column_name(solved_parameters_list[i][1])
                
            self.data_name   = data.get_name()
            self.filename    = "Multidensity_Plot" # TODO: Multidensity + Seagull Name + list of indexes (with _)

        # If the user gave a pandas dataframe
        if(solved_parameters_list[0][0] == "Pandas"):

            for i in range(self.data_length):
                self.data_x_list[i]       = data.iloc[ :  , solved_parameters_list[i][1]].to_numpy()
                self.data_name_x_list[i]  = data.columns[solved_parameters_list[i][1]]

            self.data_name   = data.name
            self.filename    = "Multidensity_Plot" 

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------

        # Plot format related
        self.bandwidth      = bandwidth   # Smaller values give more detail

        # Set the colors , line thickness, and alphas
        self.set_style(color_list          = color_list,
                       line_thickness_list = line_thickness_list,
                       color_alpha_list    = color_alpha_list,
                       set_defaults        = True)

        # Update the titles if required
        self.automatic_titles()

        # -----------------------------------------
        # Update the figure
        # -----------------------------------------
        self.automatic_size()
        self.update_figure()


    # Initialize the plot from a Seagull instance
    # I need a list of data and a list of categories
    #
    # You can do this:
    #
    # (A) Give only a list with numerical / name indexes:
    #     Each category will be the column name
    #     The numerical data is whatever is inside those columns
    #
    # (B) Give an index / name  with numeric data and an index / name with categorical data
    #     Each category is what is inside the categorical column
    #     The numerical data is filtered by category
    #
    # (C) Give a list of index / name with numeric data and a list of index / name with categorical data
    #
    #     This is an unholy mess, but I can make it work:
    #
    #          Basically, I convert this to case 2. Where I put all the numeric in order
    #          and all the categorical in order.
    #
    def init_from_seagull(self, seagull_instance:Seagull, numerical_column, categorical_column = None,
                          autoupdate_labels = True, autoupdate_filename = True):

        # Python is shit
        # C++ allows you to treat single types as list of size 1 using the pointers
        # I need to do this crap to convert it to list
        #
        # Ensure that we have a list of size one if neccesary for the variables
        if(numerical_column != None):
            if(type(numerical_column) != list):
                numerical_column = [numerical_column]
        if(categorical_column != None):
            if(type(categorical_column) != list):
                categorical_column = [categorical_column]


        # Figure out which case you have
        # (A)
        if(categorical_column == None):

            # Check that the indexes are valid
            index_validity_list = my_solvers.solve_index_list(seagull_instance, numerical_column, expected_data_type = constants.NUMERICAL_TYPES)

            # If all the indexes are valid (all elements 0 or greater)
            all_non_negative = all(x >= 0 for x in index_validity_list)
            if(all_non_negative):

                # Update the data
                self.data_length      = len(numerical_column)
                self.data_x_list      = [None] * self.data_length
                self.data_name_x_list = [None] * self.data_length     
                for i in range(self.data_length):
                    self.data_x_list[i]      = np.sort(seagull_instance.get_column_values(index_validity_list[i]))
                    self.data_name_x_list[i] = seagull_instance.get_column_name(index_validity_list[i])

                self.data_name        = seagull_instance.get_name()
                # self.data_name_y      = None ???

                # Update the labels
                if(autoupdate_labels): self.automatic_titles()

                # Update the filename
                # Seagull name + Multidensity + list of indexes (with _)
                if(autoupdate_filename):

                    string_indexes = [str(num) for num in index_validity_list]
                    join_indexes   = '_'.join(string_indexes)
                    self.filename = "Multidensity_Plot_" + seagull_instance.get_name() + "_" + join_indexes

            # If the indexes are not valid, return the error
            else:
                print()
                print("ERROR!: The indexes you gave me in the numerical column are not valid.")
                print("        This is the error code encountered for each (>=0 no error)")
                print("        "+str(index_validity_list))
                print("        I can't update the plot.")
                print()

        # (B or C)
        else:

            print("Categorical column")
            print(categorical_column)

            index_categires_validity_list = my_solvers.solve_index_list(seagull_instance,
                                                                        categorical_column,
                                                                        expected_data_type = constants.SOFT_CATEGORIES)
            
            print("Categorical validity")
            print(index_categires_validity_list)

            # Check that we actually have a categorical column
            # If all the indexes are valid (all elements 0 or greater)
            all_non_negative = all(x >= 0 for x in index_categires_validity_list)
            if(all_non_negative):
                
                # (C) convert to case (B)
                if(len(index_categires_validity_list) != 1):

                    pass

                # (B)
                else:

                    # Check that we have categories (done)
                    # Check that we have numerical data
                    index_numbers_validity_list = my_solvers.solve_index_list(seagull_instance,
                                                                              numerical_column,
                                                                              expected_data_type = constants.NUMERICAL_TYPES)

                    print("AAAAA")

                    # If all the index is valid
                    all_non_negative = all(x >= 0 for x in index_numbers_validity_list)
                    if(all_non_negative):

                        print("BBBB")

                        # Get the categories
                        my_categories = seagull_instance.get_categories(index_categires_validity_list[0])

                        print(my_categories)

                        # Filter the data for each category
                        my_filter_dictionary = seagull_instance.filter_by_category(index_categires_validity_list[0],
                                                                                   index_numbers_validity_list[0])

                        print("FILTER DICTIONARY")
                        print(my_filter_dictionary)

                        # Update the objects parameters
                        self.data_length      = len(my_categories)
                        self.data_x_list      = [None] * self.data_length
                        self.data_name_x_list = [None] * self.data_length  

                        print("Data length")
                        print(self.data_length)

                        for i in range(self.data_length):
                            self.data_x_list[i]      = np.sort(my_filter_dictionary[my_categories[i]])
                            self.data_name_x_list[i] = my_categories[i]

                        self.data_name        = seagull_instance.get_name()
                        # self.data_name_y      = None ???

                        # Update the labels
                        if(autoupdate_labels): self.automatic_titles()

                        # Update the filename
                        # Seagull name + Multidensity + list of indexes (with _)
                        if(autoupdate_filename):

                            string_indexes = [str(num) for num in index_numbers_validity_list]
                            join_indexes   = '_'.join(string_indexes)
                            self.filename = "Multidensity_Plot_" + seagull_instance.get_name() + "_" + join_indexes                    

                    else:
                        print()
                        print("ERROR!: The index in the numerical column you gave me is not valid.")
                        print("        This is the error code encountered for each (>=0 no error)")
                        print("        "+str(index_numbers_validity_list))                        
                        print("        I can't update the plot.")
                        print()

            # If the indexes are not valid, return the error
            else:
                print()
                print("ERROR!: The indexes in the categorical column you gave me are not valid.")
                print("        This is the error code encountered for each (>=0 no error)")
                print("        "+str(index_categires_validity_list))
                print("        I can't update the plot.")
                print()            

        # Set the style automatically
        self.auto_style()

        print("Styles")
        print(self.color_list)
        print(self.line_thickness_list)
        print(self.color_alpha_list)


        # Update the figure (such as init the colors automatically)
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
        self.label_x_axys   = "X"
        self.label_y_axys   = self.data_name_y

    # Switch showing extra data or not
    def show_extra_info(self, show = True):
        self.extra_info = show

    # Set the style of the plot to automatic
    def auto_style(self):
        self.set_style(set_defaults = True)

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
            if(set_defaults): self.color_list = color_manager.get_qualitative_colors(self.data_length)
        

            
        
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
                    
                    self.line_thickness_list = [1] * self.data_length
            
                # If everything is correct, use that thickness list
                else:
                    self.line_thickness_list = line_thickness_list

            # If the user gave a single thickness
            # We will use the same thickness for all the data
            else:
                self.line_thickness_list = [line_thickness_list] * self.data_length
        
        # Otherwise, init to default
        else:
            if(set_defaults): self.line_thickness_list = [2] * self.data_length 
        
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
            if(set_defaults): self.color_alpha_list = [0.9] * self.data_length        
        
    
    # Update the figure based on the data we have in the object
    def update_figure(self):

        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(self.figure_width, self.figure_height))

        # Create the density data
        # The gaussian estimator can be swapped for other estimators easily
        density_list = [None] * self.data_length
        density_data_list = [None] * self.data_length
        for i in range(self.data_length):
            density_list[i]      = stats.kde.gaussian_kde(self.data_x_list[i], bw_method = self.bandwidth)
            density_data_list[i] = density_list[i](self.data_x_list[i])

        # Calculate percentiles and mean
        percentiles_list         = [None] * self.data_length
        density_percentiles_list = [None] * self.data_length
        mean_value_list          = [None] * self.data_length
        for i in range(self.data_length):
            percentiles_list[i] = np.percentile(self.data_x_list[i], [5, 25, 50, 75, 95])
            mean_value_list[i]  = np.mean(self.data_x_list[i])
            #closest_x_index     = min(enumerate(self.data_x_list[i]), key=lambda x: abs(x[1] - percentiles_list[i]))[0]
            #density_percentiles_list = density_data_list[closest_x_index]

        for i in range(self.data_length):
            ax.plot(self.data_x_list[i], density_data_list[i],
                    color     = self.color_list[i],
                    linewidth = self.line_thickness_list[i],
                    alpha     = self.color_alpha_list[i],
                    label     = self.data_name_x_list[i])


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

                y_jitter = np.random.uniform(low = min_info_range, high = max_info_range, size=len(self.data_x_list[i]))

                # Plot the jittered points
                ax.scatter(self.data_x_list[i], y_jitter, color=self.color_list[i], alpha=0.3)

                # Calculate percentiles

                for j in range(len(percentiles_list[i])):
                    #ax.axvline(x = percentiles[j], color = self.color_list[i], linestyle = '--', linewidth=1, alpha=0.5)
                    ax.plot([percentiles_list[i][j], percentiles_list[i][j]], [min_info_range, max_info_range], 
                            color=self.color_list[i], linestyle = '--',
                            linewidth=2, alpha=0.8)


                # Add a vertical line for the mean
                #ax.axvline(x = mean_value_list[i], color = self.color_list[i], linestyle='-', linewidth = 2, alpha=0.7)

                ax.plot([mean_value_list[i], mean_value_list[i]], [min_info_range, max_info_range], 
                        color=self.color_list[i], linestyle = '-',
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
        ax.legend()

        # Update and add Plot X and Y axys
        self.label_x_axys   = self.data_name_x
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