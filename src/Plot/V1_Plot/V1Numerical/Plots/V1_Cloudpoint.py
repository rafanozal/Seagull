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

class Cloudpoint_plot(V1Plot):

    # Import the class methods
    from .methods.setters_getters import (set_data_x)

    # Default constructor
    def __init__(self, data = None, numerical_column_index:int = None, folder_path = None,  # Rearranged parameters for easy use
                 column:str = None,                                                         # Alias for numerical_column_index
                                                    # Cloudpoint plot parameters
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

        # Style related
        self.line_thickness    = 2
        self.color_line        = 'salmon'
        self.color_fill_start  = 'lightcoral'
        
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
            self.figure_width  = 5 
            self.figure_height = 10

        # Plot type
        self.type = "Cloudpoint 1D Plot"

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------


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

                        index_candidate = data.getColumnIndex(numerical_column_index)
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
                            numerical_column_index =  data.getColumnIndex(numerical_column_index)

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
            self.data_x      = np.sort(seagull_instance.getValues(target_column_index))
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
        self.figure_width  = 5 
        self.figure_height = 10

    # Set the titles automatically based on the data
    # and if the user didn't set them manually before
    def automatic_titles(self):

        self.label_title    = "Cloudpoint Plot for "  + self.data_name_x + " in " + self.data_name
        self.label_subtitle = None
        self.label_x_axys   = self.data_name_x
        self.label_y_axys   = self.data_name_y

    # Set the style of the plot (evertything related to colors)
    def style(self, line_thickness    = None, color_line      = None,
                    color_fill_start  = None):

        # Values set to None doesn't change and keep whatever was set before
        if(line_thickness    != None): self.line_thickness    = line_thickness
        if(color_line        != None): self.color_line        = color_line
        if(color_fill_start  != None): self.color_fill_start  = color_fill_start

    # Update the figure based on the data we have in the object
    def update_figure(self):
        """
        Creates a density plot using:
            1D NumPy float array for the numbers.
        """

        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(self.figure_width, self.figure_height))


        # Density Plot
        ax.plot(self.data_x, density_data, color = self.color_line, linewidth = self.line_thickness)


      
        
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