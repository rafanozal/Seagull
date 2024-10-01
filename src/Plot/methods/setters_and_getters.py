#!/usr/bin/env python3

'''

This file contain the getters and setters for the Plot class.

This only contain functions affecting only the attributes of the class.
Other functions that might change the attributes must use this attributes only.

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

# -----------------------------------------------------------------------------
# SETTERS
# -----------------------------------------------------------------------------

# Update the plot name
def set_name(self, filename):
    self.filename = filename
    self.update_figure()

# Update the plot title
def set_title(self, title):
    self.label_title = title
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