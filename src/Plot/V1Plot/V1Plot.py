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




class V1Plot(Plot):

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
        self.type = "V1 Plot"

        # Update filename, if none was given, use the HorizontalBarplot as default
        if(self.filename == None):
            self.filename = "V1_Plot"

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------
