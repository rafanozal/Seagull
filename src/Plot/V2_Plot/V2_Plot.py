
# Import the main libraries
from ..Plot     import Plot

class V2_Plot(Plot):

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
        self.type = "V2 Plot"

        #print("V2 PLOT CONSTRUCTOR")
        #print()
        #print("Plot filename: ", self.filename)
        #print("Plot folder path: ", self.folder_path)
        #print()
