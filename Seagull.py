# General libraries
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import random




class Seagull:

    """
    A class used to represent a Seagull object

    This override the Panda Dataframe functionality with syntax that is  much
    more convinient and concise.


    Attributes
    ----------
        totalRows : int
            How many rows does this data has

        totalColumns : int
            How many columns does this data has

        data : Panda Dataframe
            (Pointer) to a panda dataframe

        types : <array> string
            An array of strings telling which type of variable we have in each column

            Types can be one of the following:

            - Categorical
                - Order

            - Numerical

        totalNA : <array> int
            For each columns, how many values are missing.


    Public methods
    -------
        says(sound=None)
            Prints the animals name and what sound it makes
  
    Private methods
    -------
        countNA(int index)
            For a column given by an index, count how many NAs there are in that column
            and update the Seagull object accordingly.

        updateNA()
            For all columns, run countNA.

    """


    # Imported methods
    #
    # ---- String representations
    #      
    #      Showing the data in different ways at the console. Useful for debugging and quick overview.       

    from methods.strings_representations import print_overview

    # ---- Setters and getters
    #
    #      Accessing and setting the attributes of the class.
    from methods.setters_and_getters import getPanda, ncol, nrow

    # ---- Data Reading
    #
    #      Get information regarding different aspects of the data; but never modify it.
    from methods.data_read import getColumnNames, getColumnName, getColumn, c

    # ---- Data manipulation
    #
    #      Set the data to zeros
    #      Set the data to random values
    #      Randomize the data following the same distribution for each column
    #      Induce an error in each datacell of a 5% (default) in order to avoid indivual datapoints identifications
    from methods.data_manipulation import renameColumns, renameColumn, toInteger, toFloat
    
    # ---- Toy datasets
    #
    #      Iris dataset
    from methods.toy_datasets import set_iris

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------
    # region
    
    # An empty dataframe of given dimensions:
    # > myDF = Seagull(6,3)
    def __init__(self, totalRows, totalColumns):

        self.totalRows: int     = totalRows
        self.totalColumns: int  = totalColumns
        self.data: pd.DataFrame = pd.DataFrame(index=range(totalRows),columns=range(totalColumns))

    # endregion


    # -------------------------------------------------
    # Special methods:
    #     -__str__
    #     -__repr__
    #     -__len__
    #     -__iter__ (etc)
    # -------------------------------------------------
    # region

    # Get a copy
    def copy(self):

        newSeagul = Seagull(self.totalRows, self.totalColumns)

        for i in range(self.totalRows):
            for j in range(self.totalColumns):
                newSeagul[i,j] = self[i,j]

        newSeagul.renameColumns(self.getNames())

        return(newSeagul)



    # Override [] operator
    def __getitem__(self, xy):
            
        indexRow , indexColumn = xy

        return self.data.iloc[ indexRow , indexColumn ]

    def __setitem__(self, xy, value):

        indexRow , indexColumn = xy

        self.data.iloc[ indexRow  , indexColumn ] = value


    # endregion

    
    # -------------------------------------------------
    # region Filling the data
    # -------------------------------------------------

    # Fill the DF with zeros
    def zero(self):

      for i in range(self.totalRows):
        for j in range(self.totalColumns):

          self[i,j] = 0

    # Fill the DF with random data
    def randomize(self):

      for i in range(self.totalRows):
        for j in range(self.totalColumns):

          self[i,j] = random.random()


    # endregion
    
    

    # Check the data
    # > myDF.head()
    def head(self):

        return self.data.head()

    # Delete a column
    def dropColumn(self, index):

        self.data = self.data.drop(self.data.columns[[index]], axis=1) 


    # Set the whole column
    def setColumn(self, index, values):
        self.data.iloc[ :  , index ] = values

    # There has to be a way to override like this [,4] = ["a","b","c"]
    #def sc(self, index):
    #    self.data.iloc[ :  , index ] = values





def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = mpl.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts