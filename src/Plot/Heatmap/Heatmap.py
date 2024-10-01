#!/usr/bin/env python3

'''

This file contain the implementation of the plot class: HEATMAP

Heatmap is a subclass of the plot class, and as such it inherits all the methods from it.

[PLOT]
    |
    |--- [HEATMAP]
    |
    |--- [BARPLOT]
    |
    |--- [SCATTERPLOT]
    |
    |...

This include:

- Heatmaps
- Heatmaps with anotations in each cell
- Heatmaps with dendograms
- Heatmaps with dendograms and anotation in each cell

'''



# General libraries
import numpy as np
import matplotlib        as mpl
import matplotlib.pyplot as plt
import random
import string


# Import the main libraries
from ..Plot     import Plot
from ...Seagull import Seagull



class Heatmap(Plot):

    # Default constructor
    def __init__(self, folder_path, totalRows = 2, totalColumns = 2):
        super().__init__(folder_path)

        if(self.filename == None):
            self.filename = "Heatmap"

        self.type = "Heatmap"

        # Data related
        self.totalRows    = totalRows
        self.totalColumns = totalColumns
        self.data         = np.random.rand(totalRows, totalColumns)   # Initialize a random matrix
        self.data         = (2 * self.data) - 1                       # Scale between -1 and 1

        # Labels related
        # ---- By default create random X and Y labels
        string_length = 10
        self.row_labels = [''.join(random.choices(string.ascii_lowercase, k=string_length)) for _ in range(totalRows)]
        self.col_labels = [''.join(random.choices(string.ascii_lowercase, k=string_length)) for _ in range(totalColumns)]
        # ---- Axis labels
        self.X_axis_label = self.label_x_axys
        self.Y_axis_label = self.label_y_axys
        # ---- Legend label
        self.legend_label = self.label_legend
        # ---- Title label
        self.plot_title = self.label_title
        # ---- Inside labels
        self.annotated            = True
        self.annotation_format    = "{x:.2f}"
        self.annonation_contrasts = ("black", "white")

        # Color related
        self.color_pallette = 'YlOrRd'

        # Update the figure
        self.update_figure()

    # Show the plot using the matplotlib library
    def show(self):
        self.update_figure()
        self.figure.show()
        plt.show()

    # Update the figure based on the data we have in the object
    def update_figure(self):
        """
        Creates a heatmap using a 2D NumPy array and row and column labels.

        Parameters:
            data (numpy.ndarray): A 2D NumPy array with the data of size N rows by M columns.
            row_labels (list): A list of N strings, which will be the labels of the rows in the heatmap.
            col_labels (list): A list of M strings, which will be the labels of the columns of the heatmap.
            cmap (str): An optional argument specifying the color style of the legend. Default is 'YlOrRd'.
            legend_label (str): An optional argument specifying the label that appears in the legend.

        Returns:
            matplotlib.figure.Figure: The Figure object containing the heatmap.
        """

        # Update the basic attributes
        heatmap_data = self.data
        row_labels   = self.row_labels
        col_labels   = self.col_labels


        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(10, 20))

        # Create a heatmap using the imshow() function
        heatmap = ax.imshow(heatmap_data, cmap = self.color_pallette, aspect='auto')

        # Turn spines off and create white grid.
        ax.spines[:].set_visible(False)
        ax.set_xticks(np.arange(self.data.shape[1]+1)-.5, minor=True)
        ax.set_yticks(np.arange(self.data.shape[0]+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)        

        # Add a colorbar to the plot
        cbar = ax.figure.colorbar(heatmap, ax=ax, fraction=0.046, pad=0.04)

        # Set the tick labels for the x and y axes
        ax.set_xticks(np.arange(len(col_labels)))
        ax.set_yticks(np.arange(len(row_labels)))
        ax.set_xticklabels(col_labels)
        ax.set_yticklabels(row_labels)

        # Place the ticks marks and labels on top of the plot
        ax.tick_params(top=True,      bottom=False,
                       labeltop=True, labelbottom=False)

        # Rotate the tick labels on the x-axis
        plt.setp(ax.get_xticklabels(), rotation=25, ha="left", rotation_mode="anchor")

        # Update the labels from the Plot super-object
        self.X_axis_label = self.label_x_axys
        self.Y_axis_label = self.label_y_axys
        self.legend_label = self.label_legend
        self.plot_title   = self.label_title

        # Write the labels in the matplotlib object
        # Set the axis labels
        ax.set_xlabel(self.X_axis_label)
        ax.set_ylabel(self.Y_axis_label)
        # Set the title of the plot
        ax.set_title(self.plot_title, pad = 20)
        # Add a legend to the plot
        if self.legend_label is not None:
            cbar.ax.set_ylabel(self.legend_label, rotation=-90, va="bottom")

        # Add annotations to the heatmap if neeeded
        if(self.annotated):

            annonated_data = heatmap.get_array()
            threshold      = heatmap.norm(annonated_data.max())/2.

            # Set default alignment to center
            kw = dict(horizontalalignment = "center",
                      verticalalignment   = "center")
            
            # Get the formatter in case a string is supplied
            valfmt = mpl.ticker.StrMethodFormatter(self.annotation_format)

            # Loop over the data and create a `Text` for each "pixel".
            # Change the text's color depending on the data.
            texts = []
            for i in range(annonated_data.shape[0]):
                for j in range(annonated_data.shape[1]):
                    kw.update(color = self.annonation_contrasts[int(heatmap.norm(annonated_data[i, j]) > threshold)])
                    text = heatmap.axes.text(j, i, valfmt(annonated_data[i, j], None), **kw)
                    texts.append(text)    

        self.figure = fig

    # Update the object with the data from the seagull object
    def update_from_seagull(self, seagull_object, rowIndex = -1, columnIndex = -1):

        toReturn = -1

        # We need to figure out what type of data there's in the object.

        # Type A)
        #
        #     The data is melted and we have a row and column index
        #
        #         | Column A      | Column B       |
        # Row 01  |   Category X  |   Category Y   |
        # Row 02  |   Category Z  |   Category Y   |
        # Row                    ... 
        # Row N   |   Category X  |   Category Y   |
        #
        #     In this case we count the unique categories in each column and create a matrix
        #     with the counts. The unique categories in column A (rowIndex) will be the row labels
        #     and the unique categories in column B (columnIndex) will be the column labels.

        if (rowIndex >= 0 and columnIndex >= 0):

            # Check if we have categorical data in these indexes
            if seagull_object.isCategorical(rowIndex) and seagull_object.seagull_object.isCategorical(columnIndex):

                # Get the unique categories in the row and column indexes
                row_categories    = seagull_object.getUniqueCategories(rowIndex)
                column_categories = seagull_object.getUniqueCategories(columnIndex)

                # Create a matrix with the counts
                # At this moment is initialized with zeros
                self.data = np.zeros((len(row_categories), len(column_categories)))
                # Set the total number of rows and columns
                self.totalRows    = len(row_categories)
                self.totalColumns = len(column_categories)

                # Set the row and column labels
                self.row_labels = row_categories
                self.col_labels = column_categories

                # Create a couple of dictionaries. One for the row and one for the column
                # These contains the indexes of the categories
                rowDictionary    = {}
                columnDictionary = {}

                # Loop over the row and column categories and create the dictionaries
                for index in range(len(row_categories)):
                    rowDictionary[row_categories[index]] = index
                for index in range(len(column_categories)):
                    columnDictionary[column_categories[index]] = index

                # Loop over the rows and columns and count the number of times each combination of categories appears
                for row_index in range(len(row_categories)):
                    for column_index in range(len(column_categories)):

                        # Get the category names
                        row_category    = row_categories[row_index]
                        column_category = column_categories[column_index]

                        # Find the index of the rows that have the category in the dictionaries
                        row_ID    = rowDictionary[row_category]
                        column_ID = columnDictionary[column_category]
                        
                        # Update the data and add +1 to the count
                        self.data[row_ID, column_ID] += 1

                # In this case, the return code is 0 = Type A
                toReturn = 0

            # If we don't have categorical data, then this was a bad call
            else:
                print("Error: The row and column indexes must be categorical")
                # In this case, the return code is -1 = Error due to bad call, not categorical data

        # If we have BOTH negative indexes still
        else:

            # Then we can be in type B or type C
            if(rowIndex < 0 and columnIndex < 0):

                # If the first column has strings, then we are in type B
                if( seagull_object.isCategorical(0) ):

                    # Type B)
                    #
                    #     The data is already in matrix format, but the first column is a list of row labels
                    #
                    #         Artist  January  February  March  April  May  June  July  August  September  October  November  December
                    #   Taylor Swift        5         0      0      1    2     0     7       2          0       15         2         0
                    #     The Weeknd       13         1      2      0    1     0     0       2          0        0         3         0
                    #      Bad Bunny        0         2      0      0   16     1     0       0          0        0         0         0
                    #            SZA        0         0      0      0    0     0     0       0          0        1         0        18
                    # Kendrick Lamar        0         0      1      0   11     0     0       0          0        0         0         0
                    #
                    #     In this case, the first column is the row labels and each of the column names, without the first column, is the column labels.

                    # Get the row labels
                    self.row_labels = seagull_object.getColumn(0)
                    # Get the column labels
                    self.col_labels = seagull_object.getColumnNames()[1:]
                    
                    # Find out if in the data we have floats or we have integers
                    haveIntegers = True
                    for row in range(1, seagull_object.totalColumns):
                        if( not seagull_object.isInt(row) ):
                            haveIntegers = False


                    # Get the data
                    # Transform the data to a 2D matrix of integers if we have integers, or floats otherwise
                    if(haveIntegers == True):
                        self.data = seagull_object.getData().iloc[:, 1:].values.astype(int)
                    else:
                        self.data = seagull_object.getData().iloc[:, 1:].values.astype(float)
                    

                    # Update the total number of rows and columns
                    self.totalRows    = len(self.row_labels)
                    self.totalColumns = len(self.col_labels)

                    # In this case, the return code is 1 = Type B
                    toReturn = 1

                else:

                    # Type C)
                    #
                    #     The data is already in matrix format, and we do not have any row or column labels
                    #
                    #     January  February  March  April  May  June  July  August  September  October  November  December
                    #           5         0      0      1    2     0     7       2          0       15         2         0
                    #          13         1      2      0    1     0     0       2          0        0         3         0
                    #           0         2      0      0   16     1     0       0          0        0         0         0
                    #           0         0      0      0    0     0     0       0          0        1         0        18
                    #           0         0      1      0   11     0     0       0          0        0         0         0 
                     
                    # In this case, we don't have row labels.
                    # We can use the column names as row labels if they exist

                    # If we have column names
                    if(seagull_object.column_names != None):

                        # Set the row labels
                        self.row_labels = seagull_object.column_names

                    # Get the data
                    self.data = seagull_object.data

                    # Update the total number of rows and columns
                    self.totalRows    = len(self.data)
                    self.totalColumns = len(self.data[0])

                    # In this case, the return code is 2 = Type C
                    toReturn = 2
                  
            # Otherwise is a mistake and bad call
            else:
                print("Error: The row and column indexes must be both 0 or positive")
                print("       Otherwise, data must be already in matrix format")

                # In this case, the return code is -2 = Error due to bad call, mixing indexes and matrix format
                toReturn = -2

        # Update the figure with the new data
        self.update_figure()

        # Return the return code
        return toReturn
