#!/usr/bin/env python3

'''

This file contain the string representation functions for the subclass

    Numerical Categorical

'''


# Return the string representation of the object
def custom_str_method(self):

    parent_string = self.external_str_method()

    myString = "\n"

    myString += "----------------------------------\n"
    myString += " Type:        " + self.subtype +  "\n"
    myString += " P-value:     " + str(self.pvalue) +  "\n"
    myString += "----------------------------------\n"
    myString += " Last updated: "+ self.lastUpdate_human + "\n"
    myString += "----------------------------------\n"
    myString += " Group A:                         \n"
    myString += "\n"
    myString += " "     + self.group_a_name     + "\n"
    myString += " n = " + str(self.group_a_sample)   + "\n"
    myString += "\n"

    if(self.group_a_normality):
        myString += " Normally distributed (pv: " + str(self.group_a_normality_pvalue) + ") \n"
    else:
        myString += "/!\ Not normally distributed /!\ (pv: " + str(self.group_a_normality_pvalue) + ") \n"

    myString += "\n"

    myString += "----------------------------------\n"
    myString += " Group B:                         \n"
    myString += "\n"
    myString += " "     + self.group_b_name     + "\n"
    myString += " n = " + str(self.group_b_sample)   + "\n"
    myString += "\n"
    
    if(self.group_b_normality):
        myString += " Normally distributed (pv: " + str(self.group_b_normality_pvalue) + ") \n"
    else:
        myString += "/!\ Not normally distributed /!\ (pv: " + str(self.group_b_normality_pvalue) + ") \n"

    myString += "\n"
    myString += "----------------------------------\n"

    return parent_string + myString    

