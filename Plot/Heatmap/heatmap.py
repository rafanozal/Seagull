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
#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import string

# Own libraries
from Plot import Plot
from Seagull import Seagull


class Heatmap(Plot):

    def __init__(self, filepath, totalRows = 2, totalColumns = 2):
        super().__init__(filepath)

        self.type = "Heatmap"

        self.totalRows    = totalRows
        self.totalColumns = totalColumns
        self.data       = np.random.rand(totalRows, totalColumns)   # Initialize a random matrix
        data            = (2 * data) - 1                          # Scale between -1 and 1

        string_length = 10

        row_labels = [''.join(random.choices(string.ascii_lowercase, k=string_length)) for _ in range(totalRows)]
        col_labels = [''.join(random.choices(string.ascii_lowercase, k=string_length)) for _ in range(totalColumns)]

        self.image = None

    #def setData(self, seagullObject):



    #    self.data = seagullObject.data

    def show(self):
        self.image.show()

    def heatmap(self, ax=None, cbar_kw=None, cbarlabel="", **kwargs):
        """
        Create a heatmap from a numpy array and two lists of labels.

        ----------
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
        im = ax.imshow(self.data, **kwargs)

        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
        cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

        # Show all ticks and label them with the respective list entries.
        ax.set_xticks(np.arange(self.data.shape[1]), labels=self.col_labels)
        ax.set_yticks(np.arange(self.data.shape[0]), labels=self.row_labels)

        # Let the horizontal axes labeling appear on top.
        ax.tick_params(top=True, bottom=False,
                    labeltop=True, labelbottom=False)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
                rotation_mode="anchor")

        # Turn spines off and create white grid.
        ax.spines[:].set_visible(False)

        ax.set_xticks(np.arange(self.data.shape[1]+1)-.5, minor=True)
        ax.set_yticks(np.arange(self.data.shape[0]+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)

        self.image = im

        #return im, cbar



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
