#!/usr/bin/env python3

'''

This file contain the string representation functions for the subclass

    Numerical Univariate

'''


# Return the string representation of the object
def custom_str_method(self):

    parent_string = self.external_str_method()

    myString = "\n"

    myString += "----------------------------------\n"
    myString += " Type:        " + self.subtype     + "\n"
    myString += " Sample Size: " + str(self.sample_size) + "\n"
    myString += "----------------------------------\n"
    myString += " Last updated: "+ self.lastUpdate_human + "\n"
    myString += "----------------------------------\n"

     # Descriptive statistics
    myString += "\n"
    myString += " -- Percentiles -- \n"
    myString += "\n"
    myString += "p05:    " + str(self.p05)    + "\n"
    myString += "p25:    " + str(self.p25)    + "\n"
    myString += "median: " + str(self.median) + "\n"
    myString += "p75:    " + str(self.p75)    + "\n"
    myString += "p95:    " + str(self.p95)    + "\n"
    myString += "\n"
    myString += " -- Measures -- \n"
    myString += "\n"
    myString += "mean:   " + str(self.mean)   + "\n"
    myString += "std:    " + str(self.std)    + "\n"
    myString += "var:    " + str(self.var)    + "\n"
    myString += "\n"
    myString += " -- Ranges -- \n"
    myString += "\n"
    myString += "range:  " + str(self.range)  + "\n"
    myString += "iqr:    " + str(self.iqr)    + "\n"
    myString += "min:    " + str(self.min)    + "\n"
    myString += "max:    " + str(self.max)    + "\n"
    myString += "\n"
    myString += " -- Plots -- \n"
    myString += "\n"

    if(self.folder_path != None):
        myString += "Density plot:  " + str(self.density.get_folder_path()) + "/" + str(self.density.get_filename()) + "\n"
    else:
        myString += "Density plot:  Folder path is not initialize, can't save the plot\n"

    myString += "\n"
    myString += " -- Distributions -- \n"
    myString += "\n"
    myString += "        Normal: N(μ = " + str(self.normal_fit_mu) + " , σ = " + str(self.normal_fit_sigma) + " ) \n"
    myString += "\n"
    myString += "            Shapiro-Wilk:       " + str(self.normal_fit_shapiro[0])    + " (pv: " + str(self.normal_fit_shapiro[1])    + " , st: " + str(self.normal_fit_shapiro[2])    + " )" + "\n"
    myString += "            Kolmogorov-Smirnov: " + str(self.normal_fit_kolmogorov[0]) + " (pv: " + str(self.normal_fit_kolmogorov[1]) + " , st: " + str(self.normal_fit_kolmogorov[2]) + " )" + "\n"
    myString += "            Anderson-Darling:         (st: " + str(self.normal_fit_anderson[1]) + ")\n"
    
    for i in range(len(self.normal_fit_anderson[0])):
        myString += "                " + str(self.normal_fit_anderson[0][i][0]) + "% : " + str(self.normal_fit_anderson[0][i][2]) + " cv: " + str(self.normal_fit_anderson[0][i][1]) + "\n"

    myString += "\n"



    myString += "uniform_fit:     " + str(self.uniform_fit) + "\n"
    myString += "exponential_fit: " + str(self.exponential_fit) + "\n"
    myString += "poisson_fit:     " + str(self.poisson_fit) + "\n"
    myString += "binomial_fit:    " + str(self.binomial_fit) + "\n"
    myString += "weibull_fit:     " + str(self.weibull_fit) + "\n"
    myString += "lognormal_fit:   " + str(self.lognormal_fit) + "\n"
    myString += "gamma_fit:       " + str(self.gamma_fit) + "\n"
    myString += "beta_fit:        " + str(self.beta_fit) + "\n"
    myString += "chisquared_fit:  " + str(self.chisquared_fit) + "\n"
    myString += "\n"
    myString += "----------------------------------\n"

    return parent_string + myString    

