
# Import the main libraries
from ..Plot     import Plot

class VN_Plot(Plot):

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
        self.type = "VN Plot"

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------
        self.data_x_list = None
