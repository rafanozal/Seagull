# Plot/plot.py



class Plot:

    def __init__(self, filepath):

        self.filepath = filepath        # Where in this the image for this plot is stored
        self.type     = "None"          # What type of plot it is (e.g. "scatter", "histogram", etc)

    #def plot(self):
    #    pass


    def __str__(self):

        myString = "Plot object: \n"

        myString += "Filepath: " + self.filepath + "\n"
        myString += "Type: " + self.type + "\n"

        return myString