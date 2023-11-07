class Plot:

    def __init__(self, filepath, type):

        self.filepath = filepath
        self.type     = type



    def __str__(self):

        myString = "Plot object: \n"

        myString += "Filepath: " + self.filepath + "\n"
        myString += "Type: " + self.type + "\n"

        return myString