#!/usr/bin/env python3

'''

This file contain the getters and setters for the Plot class.

This only contain functions affecting only the attributes of the class.
Other functions that might change the attributes must use this attributes only.


        self.data_name     = "<Default data name>" # These are just defaults that you should never see
        self.data_name_x   = "<X>"                 # The final instances of plots are the one responsible
        self.data_name_y   = "<Y>"                 # for initiating and updating these values properly.
        self.data_name_z   = "<Z>"
        self.legend_name_z = "<Zelda>"

        # ------------------------------------------
        # Labels
        # ------------------------------------------

        self.label_title:str      = plot_title     # Initialize the main labels to be empty (None) by default
        self.label_subtitle:str   = plot_subtitle
        self.label_y_axys:str     = plot_y_Label
        self.label_x_axys:str     = plot_x_label
        self.label_legend:str     = plotLegend

'''
    




    
# -----------------------------------------------------------------------------
# GETTERS
# -----------------------------------------------------------------------------

# Get the figure object (as in the matplotlib object)
def get_figure(self):
    return self.figure

# Get the figure size
def get_size(self):
    return [self.figure_width, self.figure_height]


# Get the plot folder path
def get_folder_path(self):
    return(self.folder_path)

# Get the plot filename
def get_filename(self):
    return(self.filename)



# -----------------------------------------------------------------------------
# SETTERS
# -----------------------------------------------------------------------------

# Update the plot folder path
def set_folder_path(self, folder_path):
    self.folder_path = folder_path
    self.update_figure()

# Update the plot filename
def set_filename(self, filename):
    self.filename = filename
    self.update_figure()

change_filename = set_filename

# Update the plot data name
def set_data_name(self, data_name):
    self.data_name = data_name
    self.update_figure()

# Update the plot data X, Y and Z names
def set_data_name_x(self, data_name_x):
    self.data_name_x = data_name_x
    self.update_figure()

def set_data_name_y(self, data_name_y):
    self.data_name_y = data_name_y
    self.update_figure()

def set_data_name_z(self, data_name_z):
    self.data_name_z = data_name_z
    self.update_figure()




# Update the plot title and subtitle
def set_title(self, title):
    self.label_title = title
    self.update_figure()

def set_subtitle(self, subtitle):
    self.label_subtitle = subtitle
    self.update_figure()

# Update the X label
def set_x_label(self, x_label):
    self.label_x_axys = x_label
    self.update_figure()

# Update the Y label
def set_y_label(self, y_label):
    self.label_y_axys = y_label
    self.update_figure()

# Update the plot legend
def set_legend(self, legend):
    self.label_legend = legend
    self.update_figure()

# Update figure size
def set_size(self, width, height):
    self.figure_width  = width
    self.figure_height = height
    self.update_figure()    