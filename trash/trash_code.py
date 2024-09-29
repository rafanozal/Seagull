

    def heatmap(self, cbar_kw=None, cbarlabel="", **kwargs):
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

        cbar_kw
            A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.

        cbarlabel
            The label for the colorbar.  Optional.

        **kwargs
            All other arguments are forwarded to `imshow`.

        """

        # Create a figure and axis object
        fig, ax = plt.subplots()

        # Set the colorbar defaults
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