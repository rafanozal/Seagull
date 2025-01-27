# Plot/Plot.py

# ----------------------------------------------------
# IMPORTS
#
# Subclasses will use all these
# TODO: (Can't make subclasses import from parent class libraries)
# ----------------------------------------------------

from abc import ABC, abstractmethod           # Abstract class library

# General libraries
import numpy as np
import matplotlib.pyplot      as plt
import matplotlib.patheffects as PathEffects
import matplotlib.colors as mcolors           # Import the mathplot colors
import random
import string

# Import the auxiliary libraries
import lib.color_manager as mypaint           # Import the color manager

class Plot(ABC):

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
    from .methods.setters_and_getters import(
        get_figure, get_size,
        get_folder_path,
        get_filename, 
        set_folder_path,
        set_filename, change_filename,
        set_data_name, set_data_name_x, set_data_name_y, set_data_name_z,
        set_title, set_subtitle,
        set_x_label, set_y_label, set_legend,
        set_size
    )

    # ----------------------------------
    # Constructor
    # ----------------------------------

    def __init__(self, folder_path = None, filename = None,
                 plot_title   = None, plot_subtitle = None,
                 plot_y_Label = None, plot_x_label  = None,
                 plot_legend  = None,
                 image_w_size = None, image_h_size = None):

        # ------------------------------------------
        # Type
        # ------------------------------------------

        self.type:str         = "Plot"             # What type of plot it is (e.g. "scatter", "histogram", etc)

        # ------------------------------------------
        # Folder and Filename
        # ------------------------------------------

        self.folder_path:str  = folder_path        # Where in this the image for this plot is stored, this is a folder
        self.filename:str     = filename           # The name of the files which will be saved
                                                   #     If the name is "myPlot", then the files will be saved as:
                                                   #         myPlot.png
                                                   #         myPlot.pdf
                                                   #         myPlot.svg
                                                   #     All of these will be inside filepath folder

        print("PLOT CONSTRUCTOR")
        print()
        print("Plot filename: ", self.filename)
        print("Plot folder path: ", self.folder_path)
        print()

        # ------------------------------------------
        # Figure
        # ------------------------------------------
        self.manual_size:bool  = False             # If someone changed the size manually

        self.figure            = None              # Initialize the figure to the default (fig)
        self.axes              = None              # Initialize the axes object (ax)
        self.figure_width:int  = image_w_size      # W and H size of the figure
        self.figure_height:int = image_h_size

        # Update default size if needed
        if(self.figure_width == None):
            self.figure_width  = 15
        else:
            self.manual_size   = True

        if(self.figure_height == None):
            self.figure_width  = 10
        else:
            self.manual_size   = True

        # ------------------------------------------
        # Data
        # ------------------------------------------
        self.data_name     = "<Default data name>" # These are just defaults that you should never see

        # ------------------------------------------
        # Labels
        # ------------------------------------------

        self.label_title:str      = plot_title     # Initialize the main labels to be empty (None) by default
        self.label_subtitle:str   = plot_subtitle
        self.label_y_axys:str     = plot_y_Label
        self.label_x_axys:str     = plot_x_label
        self.label_legend:str     = plot_legend
        
        # ------------------------------------------
        # Theme
        # by default is the "white" theme option
        # ------------------------------------------
        #     Name
        self.theme_name = "white"
        #     Background color
        self.theme_background_color = mypaint.color_to_hex("white")
        self.theme_background_alpha = 0.0
        #     Axys X and Y Line color
        self.theme_axys_line_color  = mypaint.color_to_hex("black")
        self.theme_axys_line_alpha  = 1.0
        #     Axys X and Y Major breaks color
        self.theme_x_major_breaks_color = mypaint.color_to_hex("white")
        self.theme_y_major_breaks_color = "0.7"
        self.theme_x_major_breaks_alpha = 0.0
        self.theme_y_major_breaks_alpha = 1.0
        #     Legend position
        self.theme_legend_position    = "right"
        #     Ticks size in both X and Y
        self.theme_ticks_size         = 3
        #     Font size for ticks
        self.theme_ticks_x_font_size  = 12
        self.theme_ticks_y_font_size  = 12
        #     Inner panel border
        self.theme_inner_panel_border_color = mypaint.color_to_hex("black")
        self.theme_inner_panel_border_alpha = 1.0

    # ----------------------------------
    # Abstract methods
    # To be implemented by instanciable subclasses
    # ----------------------------------    
    @abstractmethod
    def update_figure(self):
        """
        Update the state of the object.
        Subclasses are expected to implement this method.
        """
        pass
    @abstractmethod
    def automatic_filename(self):
        pass
    @abstractmethod
    def automatic_titles(self):
        pass
    @abstractmethod
    def automatic_size(self):
        pass

    # ----------------------------------
    # Class methods
    # ----------------------------------
    __str__ = custom_str_method

    # ----------------------------------
    # Show the plot
    # ----------------------------------
    # Show the plot using the matplotlib library
    def show(self):
        self.update_figure()
        self.figure.show()
        plt.show()
    
    # ----------------------------------
    # Seters and getters
    # ----------------------------------
    def set_filename(self, filename:str):
        self.filename = filename

    # ----------------------------------
    # Saving the plot in disk
    # ----------------------------------

    # Save the plot using the matplotlib library
    def save(self, savepath = None, savePNG = True, savePDF = True, saveSVG = True, saveTXT = False):

        self.update_figure()

        # Tell where are you saving the plot
        print("Saving... ", self.folder_path + "/" + self.filename + ".*")

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

    # ----------------------------------
    # Themes of a plot
    # ----------------------------------
    def set_theme(self, theme:str):
        
        if(theme=="white"):

            #     Name
            self.theme_name = "white"
            #     Background color
            self.theme_background_color = mcolors.white
            self.theme_background_alpha = 0.0
            #     Axys X and Y Line color
            self.theme_axys_line_color  = mcolors.black
            self.theme_axys_line_alpha  = 1.0
            #     Axys X and Y Major breaks color
            self.theme_x_major_breaks_color = mcolors.white
            self.theme_y_major_breaks_color = "0.7"
            self.theme_x_major_breaks_alpha = 0.0
            self.theme_y_major_breaks_alpha = 1.0
            #     Legend position
            self.theme_legend_position    = "right"
            #     Ticks size in both X and Y
            self.theme_ticks_size         = 3
            #     Font size for ticks
            self.theme_ticks_x_font_size  = 12
            self.theme_ticks_y_font_size  = 12
            #     Inner panel border
            self.theme_inner_panel_border_color = mcolors.black        
            self.theme_inner_panel_border_alpha = 1.0

        elif(theme=="no-grid"):

            #     Name
            self.theme_name = "no-grid"
            #     Background color
            self.theme_background_color = mcolors.white
            self.theme_background_alpha = 0.0
            #     Axys X and Y Line color
            self.theme_axys_line_color  = mcolors.black
            self.theme_axys_line_alpha  = 0.0
            #     Axys X and Y Major breaks color
            self.theme_x_major_breaks_color = mcolors.white
            self.theme_y_major_breaks_color = "0.7"
            self.theme_x_major_breaks_alpha = 0.0
            self.theme_y_major_breaks_alpha = 0.0
            #     Legend position
            self.theme_legend_position    = "right"
            #     Ticks size in both X and Y
            self.theme_ticks_size         = 0
            #     Font size for ticks
            self.theme_ticks_x_font_size  = 0
            self.theme_ticks_y_font_size  = 0
            #     Inner panel border
            self.theme_inner_panel_border_color = mcolors.black        
            self.theme_inner_panel_border_alpha = 0.0

        else:
            print("WARNING!: Theme " + theme + " not found")
            print("         : Using default theme 'white'")

            #     Name
            self.theme_name = "white"
            #     Background color
            self.theme_background_color = mcolors.white
            self.theme_background_alpha = 0.0
            #     Axys X and Y Line color
            self.theme_axys_line_color  = mcolors.black
            self.theme_axys_line_alpha  = 1.0
            #     Axys X and Y Major breaks color
            self.theme_x_major_breaks_color = mcolors.white
            self.theme_y_major_breaks_color = "0.7"
            self.theme_x_major_breaks_alpha = 0.0
            self.theme_y_major_breaks_alpha = 1.0
            #     Legend position
            self.theme_legend_position    = "right"
            #     Ticks size in both X and Y
            self.theme_ticks_size         = 3
            #     Font size for ticks
            self.theme_ticks_x_font_size  = 12
            self.theme_ticks_y_font_size  = 12
            #     Inner panel border
            self.theme_inner_panel_border_color = mcolors.black        
            self.theme_inner_panel_border_alpha = 1.0