#!/usr/bin/env python3

'''

This file contain the string representation functions for the Analysis class

The main class is almost empty, so this method doesn't do much by itself.
However the children class inherit from it and add to the information.

'''


# Return the string representation of the object
def external_str_method(self):

    myString = "\n"

    myString += "----------------------------------\n"
    myString += "        I'm an Analysis!\n"
    myString += "----------------------------------\n"
    myString += "\n"
    myString += "----------------------------------\n"
    if(self.folder_path == None):
        myString += "Filepath: " + "None" + "\n"
    else:
        myString += "Filepath: " + self.folder_path + "\n"


    if(self.filename == None):
        myString += "Filename:     " + "None"        + "\n"
    else:
        myString += "Filename:     " + self.filename     + "\n"
            
    myString += "----------------------------------\n"
    myString += " Type:     " + self.type + "\n"
    myString += "----------------------------------\n"



    return myString