# Plot/Plot.py

# ----------------------------------------------------
# IMPORTS
#
# Subclasses will use all these
# TODO: (Can't make subclasses import from parent class libraries)
# ----------------------------------------------------



class Plot:

    """
    A class representing a plot object.

    Plot objects are INDEPENDENT from a Seagull object. Plot object can be
    initialized given a Seagull object. But this library can be used without
    Seagull as well, just by giving the data to the plot. Initializing from
    Seagull only extract the data from Seagull and give it to the Plot object
    to be constructed as usually does as default.

    Plots are much more than a figure. Plots have labels, color palette, and
    many other things that make them a unique class.

    Attributes:
        folder_path    (str):        The directory where the image for this plot is stored.
        type           (str): ("")   The type of plot (e.g., "scatter", "histogram").
        filename       (str): (None) The name of the file to be saved. If provided, the plot will be saved with this
                                     filename in the formats .png, .pdf, and .svg inside the folder_path.

        figure:               (None) The figure object of the plot.
        figure_width   (int): (10)   X size of the figure
        figure_height  (int): (15)   Y size of the figure

        label_title    (str): ("")   The main title label of the plot.
        label_subtitle (str): ("")   The subtitle label of the plot.
        label_y_axys   (str): ("")   The label for the y-axis of the plot.
        label_x_axys   (str): ("")   The label for the x-axis of the plot.
        label_legend   (str): ("")   The label for the legend of the plot.

        

    Methods:
        start: Simulates starting the car.
        display_info: Prints information about the car.
    """

    # Imported methods
    #
    # ---- String representations
    #      
    #      Showing the data in different ways at the console. Useful for debugging and quick overview.
    from .methods.strings_representations import custom_str_method

    # ---- Setters and getters
    #
    #      Accessing and setting the attributes of the class.
    from .methods.setters_and_getters import  get_figure, get_size, set_name, set_title, set_x_label, set_y_label, set_legend, set_size

    # ----------------------------------
    # Constructor
    # ----------------------------------

    def __init__(self, folder_path, filename = None):

        self.folder_path: str = folder_path        # Where in this the image for this plot is stored, this is a folder

        self.type:str         = ""                 # What type of plot it is (e.g. "scatter", "histogram", etc)

        self.filename:str     = filename           # The name of the files which will be saved
                                                   #     If the name is "myPlot", then the files will be saved as:
                                                   #         myPlot.png
                                                   #         myPlot.pdf
                                                   #         myPlot.svg
                                                   #     All of these will be inside filepath folder

        # ------------------------------------------
        # Figure
        # ------------------------------------------

        self.figure            = None              # Initialize the figure to the default
        self.figure_width:int  = 15                # W and H size of the figure
        self.figure_height:int = 10

        # ------------------------------------------
        # Labels
        # ------------------------------------------

        self.label_title:str      = ""             # Initialize the main labels to be empty
        self.label_subtitle:str   = ""
        self.label_y_axys:str     = ""
        self.label_x_axys:str     = ""
        self.label_legend:str     = ""
        

    # ----------------------------------
    # Plots updates
    # These are done by the individual instances of each plot type
    # ----------------------------------
    def update_figure(self):
        pass
    def automatic_size(self):
        pass

    # ----------------------------------
    # Class methods
    # ----------------------------------
    __str__ = custom_str_method

    # ----------------------------------
    # Saving the plot in disk
    # ----------------------------------

    # Save the plot using the matplotlib library
    def save(self, savePNG = True, savePDF = True, saveSVG = True, saveTXT = False, saveHTML = False):

        self.update_figure()

        # For each of the possible formats, save the figure
        if(savePNG):
            self.figure.savefig(self.folder_path + "/" + self.filename + ".png")

        if(savePDF):
            self.figure.savefig(self.folder_path + "/" + self.filename + ".pdf")

        if(saveSVG):
            self.figure.savefig(self.folder_path + "/" + self.filename + ".svg")

        # For each of the possible extra format, also save the figure
        if(saveTXT):
            print("TODO:Save the TXTs")
        if(saveHTML):
            print("TODO:Save the HTMLs")