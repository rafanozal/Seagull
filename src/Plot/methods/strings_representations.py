#!/usr/bin/env python3

'''

This file contain the string representation functions for the Plot class

'''


# Return the string representation of the object
def custom_str_method(self):

    myString = "Plot object: \n"
    myString += "\n"
    myString += "----------------------------------\n"
    myString += "Filepath: " + self.folder_path + "\n"

    if(self.filename == None):
        myString += "Filename:     " + "None"        + "\n"
    else:
        myString += "Filename:     " + self.filename     + "\n"
            
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
