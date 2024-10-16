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
    def __init__(self, **kwargs):
        
        # -----------------------------------------
        # Do the parent constructor first
        # -----------------------------------------
        super().__init__(**kwargs)  # Pass common parameters to the parent constructor

        # -----------------------------------------
        # Update the parent class attributes second
        # -----------------------------------------

        # Plot type
        self.type = "V1 Plot"

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------
        self.data_x = None
