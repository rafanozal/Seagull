
# Import the main libraries
from ..Plot     import Plot

class V1_Plot(Plot):

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

        #print("V1 PLOT CONSTRUCTOR")
        #print()
        #print("Plot filename: ", self.filename)
        #print("Plot folder path: ", self.folder_path)
        #print()
