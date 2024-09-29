# Plot/Plot.py

class Plot:

    # ----------------------------------
    # Constructor
    # ----------------------------------

    def __init__(self, folder_path, name = None):

        self.folder_path = folder_path        # Where in this the image for this plot is stored, this is a folder

        self.type        = "None"             # What type of plot it is (e.g. "scatter", "histogram", etc)

        self.name        = name               # The name of the files which will be saved
                                              #     If the name is "myPlot", then the files will be saved as:
                                              #         myPlot.png
                                              #         myPlot.pdf
                                              #         myPlot.svg
                                              #     All of these will be inside filepath folder

        self.figure      = None               # Initialize the figure to the default

        self.label_title      = ""            # Initialize the main labels to be empty
        self.label_subtitle   = ""
        self.label_y_axys     = ""
        self.label_x_axys     = ""
        self.label_legend     = ""
        


    # Update the plot
    # This is done by the individual instances of each plot type
    def update_figure(self):
        pass

    # ----------------------------------
    # Class methods
    # ----------------------------------

    # Return the string representation of the object
    def __str__(self):

        myString = "Plot object: \n"
        myString += "\n"
        myString += "----------------------------------\n"
        myString += "Filepath: " + self.folder_path + "\n"

        if(self.name == None):
            myString += "Name:     " + "None"        + "\n"
        else:
            myString += "Name:     " + self.name     + "\n"
            
        myString += "----------------------------------\n"
        myString += "Type:     " + self.type + "\n"

        myString += "----------------------------------\n"
        myString += "  Main labels:                    \n"
        myString += "----------------------------------\n"
        myString += "Title:     " + self.label_title    + "\n"
        myString += "Subtitle:  " + self.label_subtitle + "\n"
        myString += "Y-axys:    " + self.label_y_axys   + "\n"
        myString += "X-axys:    " + self.label_x_axys   + "\n"
        myString += "Legend:    " + self.label_legend   + "\n"


        return myString

    # ----------------------------------
    # Saving the plot in disk
    # ----------------------------------

    # Save the plot using the matplotlib library
    def save(self, savePNG = True, savePDF = True, saveSVG = True):

        self.update_figure()

        # For each of the possible formats, save the figure
        if(savePNG):
            self.figure.savefig(self.folder_path + "/" + self.name + ".png")

        if(savePDF):
            self.figure.savefig(self.folder_path + "/" + self.name + ".pdf")

        if(saveSVG):
            self.figure.savefig(self.folder_path + "/" + self.name + ".svg")

    # ----------------------------------
    # Getters and setters
    # ----------------------------------

    # Get the figure object (as in the matplotlib object)
    def get_figure(self):
        return self.figure

    # Update the plot name
    def set_name(self, name):
        self.name = name
        self.update_figure()

    # Update the plot title
    def set_title(self, title):
        self.label_title = title
        self.update_figure()

    # Update the X label
    def set_x_label(self, x_label):
        self.label_x_axys = x_label
        self.update_figure()

    # Update the Y label
    def set_y_label(self, y_label):
        self.label_y_axys = y_label
        self.update_figure()

    # Update the plot legend
    def set_legend(self, legend):
        self.label_legend = legend
        self.update_figure()