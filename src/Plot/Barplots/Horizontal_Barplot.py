#!/usr/bin/env python3

'''

This file contain the implementation of the plot class: HORIZONTAL BARPLOT

Horizontal barplot is a subclass of the plot class, and as such it inherits all the methods from it.

[PLOT]
    |
    |--- [HEATMAP]
    |
    |--- [BARPLOTS]
                 |
                 | --- [HORIZONTAL]
                 | --- [VERTICAL]
    |
    |--- [SCATTERPLOT]
    |
    |...

This include:

- Horizontal barplots
- Horizontal barplots with annotations in each bar
- Horizontal barplots normalized

'''

# General libraries
import numpy as np
import matplotlib.pyplot      as plt
import matplotlib.patheffects as PathEffects
import random
import string

# Import the auxiliary libraries
import lib.color_manager as mytools

# Import the main libraries
from ..Plot     import Plot
from ...Seagull import Seagull




class Horizontal_Barplot(Plot):

    # Default constructor
    def __init__(self, folder_path, totalColumns = 5):

        # -----------------------------------------
        # Do the parent constructor first
        # -----------------------------------------
        super().__init__(folder_path)

        # -----------------------------------------
        # Update the parent class attributes second
        # -----------------------------------------

        # Default figure size, can and will be updated automatically later
        self.figure_width  = 7 
        self.figure_height = 10

        # Plot type
        self.type = "Horizontal Barplot"

        # Update filename, if none was given, use the HorizontalBarplot as default
        if(self.filename == None):
            self.filename = "HorizontalBarplot"

        # Figure stays the same, to be updated later

        # Plot labels stay the same, to be updated later
        

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------

        # Data related
        self.totalColumns = totalColumns
        self.data         = np.random.rand(totalColumns)   # Initialize a random array
        self.data         = (2 * self.data) - 1            # Scale between -1 and 1

        # Labels related
        # ---- By default create random labels of 10 characters
        string_length   = 10
        self.col_labels = [''.join(random.choices(string.ascii_lowercase, k=string_length)) for _ in range(totalColumns)]
        self.col_digits = self.data

        # ---- Format
        self.annotated            = True
        self.annotation_format    = "{x:.2f}"
        self.annonation_contrasts = ("black", "white")

        # Color related
        self.color_pallette       = 'dimgrey'
        self.column_colors        = mytools.color_to_hex(self.color_pallette)

        # -----------------------------------------
        # Update the figure
        # -----------------------------------------
        self.automatic_size()
        self.update_figure()


    # Show the plot using the matplotlib library
    def show(self):
        self.update_figure()
        self.figure.show()
        plt.show()

    # Automic figure size
    def automatic_size(self):
        """
        Counts the amount of amount of colums and font sizes
        and attempt to create a reasonable size that makes the
        plot look good enought.

        Manual addjustment can be done with the method:

            >myPlot.set_size(width, height)

        """

        automatic_height = self.totalColumns           # One unit size per column
        automatic_width  = automatic_height            # Make a square figure if size is smaller than 5
        if(automatic_height > 5): automatic_width = 5  # Otherwise, lock the width and let it grow vertically

        # Now we need to adjust width for long labels
        # -- Measure the bigest label we have
        max_string_length   = max(len(s) for s in self.col_labels)
        # -- If it is bigger than 4, we need to give +2 unit for each 5 characters
        if(max_string_length > 4):
            automatic_width = automatic_width + 2*((automatic_width + 5 - 1) // 5)

        self.set_size(automatic_width, automatic_height)


    # Update the figure based on the data we have in the object
    def update_figure(self):
        """
        Creates an horizontal barplot using:
            1D NumPy float array for the numbers.
            1D str array for the labels.

        """

        # Update the basic attributes
        #barplot_data = self.data
        #col_labels   = self.col_labels

        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(self.figure_width, self.figure_height))

        # Calculate bar height based on the number of labels and desired spacing
        # bar_height = 0.8 / len(self.col_labels)

        # Horizontal Bar Plot
        #plt.barh(col_labels,  barplot_data)
        #ax.barh(self.col_labels, self.data, height = bar_height)
        ax.barh(self.col_labels, self.data)

        # Add padding between axes and labels
        ax.xaxis.set_tick_params(pad=7)
        ax.yaxis.set_tick_params(pad=12)

        # Add auxiliary grid line
        ax.grid(color ='grey',
                linestyle ='-.', linewidth = 0.5,
                alpha = 0.2)

        # barh rotate a bar in one direction, which by default seems counterintuitive
        # This line reverse the order of the bars
        ax.invert_yaxis()

        # Add annotation to bars (if needed)
        if(self.annotated):

            # For each column
            for bar in ax.patches:

                # Get the width of the bar (positive or negative)
                bar_width  = bar.get_width()
                bar_height = bar.get_height()

                # Set the position of the text (left or right) based on the bar width (negative or positive)
                if bar_width < 0:
                    # Place text to the left of the bar
                    text_x = bar_width - 0.005 
                else:
                    # Place text to the right of the bar
                    text_x = bar_width + 0.005

                # The y position is the vertical center of the bar
                text_y = bar.get_y() + bar_height / 2

                # Display the text annotation
                bars_labels = ax.text(text_x, text_y, f'{bar_width:.2f}', 
                                      va='center', ha='right' if bar_width < 0 else 'left',
                                      fontsize=10, fontweight='bold',
                                      color='whitesmoke')
                
                # Add a black border around the text
                bars_labels.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='#343434')])

        # Add Plot Title
        ax.set_title(self.label_title, loc='left', )

        # Add Plot X and Y axys
        ax.set_xlabel(self.label_x_axys)
        ax.set_ylabel(self.label_y_axys)


        # TODO: Multicategorical barplots
        # Add a legend to the plot
        #if self.legend_label is not None:
        #    cbar.ax.set_ylabel(self.legend_label, rotation=-90, va="bottom")

        # Uodate the figure internatl object
        self.figure = fig