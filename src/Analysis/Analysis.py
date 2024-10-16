# General libraries
import numpy  as np
import pandas as pd
import random

from scipy import stats

# Constants
from src import constants

# Main class declaration
class Analysis:

    """
    A class used to represent the Analysis object

    This is a wrapper of many common statistical analysis and machine learning methods

    1. Categorical Data

        Categorical with Categorical:
            Chi-Squared Test (χ² Test): Used to determine whether there is a significant association between two categorical variables.
            Fisher’s Exact Test: Used for small sample sizes, providing an exact p-value for the association between categorical variables.

    2. Numerical Data

        Numerical univariate:

            
        Numerical with Numerical:
            Correlation Analysis (e.g., Pearson, Spearman): Measures the strength and direction of the relationship between two numerical variables.
            Regression Analysis:
                Linear Regression: Models the linear relationship between a dependent variable and one or more independent variables.
                Multiple Regression: Extends linear regression to include multiple independent variables.

    3. Numerical with Categorical

        T-test:
            Independent Samples T-test: Compares the means of two independent groups.
            Paired Samples T-test:      Compares the means from the same group at different times (or under different conditions).

        ANOVA (Analysis of Variance):
            One-way ANOVA:              Tests differences between the means of three or more independent groups.
            Two-way ANOVA:              Examines the influence of two different categorical independent variables on one dependent variable.

        Covariance Analysis (ANCOVA):   Used to compare categorical and continuous variables while controlling for the effects of additional continuous variables that can affect the dependent variable.

    4. Sorted Categorical Data (Ordinal)

        Ordinal with Ordinal:
            Spearman’s Rank Correlation Coefficient: Non-parametric measure of rank correlation, assessing how well the relationship between two variables can be described using a monotonic function.

        Ordinal with Categorical:
            Mann-Whitney U Test: Non-parametric test for assessing whether two independent samples originate from the same distribution.
            Kruskal-Wallis Test: Non-parametric version of ANOVA, used when the assumptions of ANOVA are not met.

        Ordinal with Numerical:
            Point-Biserial Correlation: Measures the strength and direction of the association that exists between one continuous variable and one binary categorical variable.

    """

    # Imported methods
    # ---- Setters and getters
    from .methods.setters_getters import (
        set_folder_path, get_folder_path,
        set_filename, get_filename
    )

    # ---- String representations
    from .methods.strings_representations import external_str_method
    # ---- Static methods
    from .methods.statics_methods import p_value_to_significance, normality, kolmogorov_smirnov, anderson_darling

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------

    def __init__(self, folder_path = None, filename = None):
        
        # ---------------------------------------------------------------------
        # Where is this analysis saved and how it is called
        # ---------------------------------------------------------------------
        self.folder_path:str  = folder_path        # Where in this the analysis for this data stored, this is a folder

        self.filename:str     = filename           # The name of the files which will be saved
                                                   #     If the name is "myAnalysis", then the files will be saved as:
                                                   #         myAnalysis.txt
                                                   #         myAnalysis.html
                                                   #     All of these will be inside filepath folder

        # ---------------------------------------------------------------------
        # What type of analysis is this
        # ---------------------------------------------------------------------
        self.type:str         = "Non-init"         # What type of analysis it is (e.g. "T-test", "Regression", etc) 
        
        # ---------------------------------------------------------------------
        # To whom is this analysis done
        # ---------------------------------------------------------------------
        self.tablename:str    = "No_Table_Name"    # The name of the table upon which this analysis is performed

        # ---------------------------------------------------------------------
        # When was it done last time
        # ---------------------------------------------------------------------
        self.lastUpdate           = 0        # Last time this analysis was updated
        self.lastUpdate_human:str = "Never!" # Time in human readable format
        


    # -------------------------------------------------
    # Class methods:
    #     -__str__
    #     -__repr__
    #     -__len__
    #     -__iter__ (etc)
    # -------------------------------------------------
    # region

    # String

    def custom_str_method(self):
        # Call external function,
        # otherwise __super__ goes wonkers if
        # custom_str_method is defined outside the class body
        # and called later subclasses
        myString = self.external_str_method()
        return myString

    __str__ = custom_str_method

    # Copy
    def copy(self):

        return(0)

    # Override [] operator
    def __getitem__(self, xy):
            
        return(0)

    def __setitem__(self, xy, value):

        return(0)

    # endregion

    # ----------------------------------
    # Saving the analysis in disk
    # ----------------------------------
    def save(self, saveTXT = True, saveHTML = True):

        # If the path for the folder is define continue        
        if(self.folder_path != None):

            # If you want to save the TXT or the HTML continue
            if(saveTXT or saveHTML):

                # When you want to save the HTML
                if(saveHTML):

                    print("Saving HTML report...")

                    # Load the CSS template
                    css_template  = ""
                    css_file_path = constants.CSS_SEAGULL_STYLE
                    with open(css_file_path, 'r', encoding='utf-8') as file:
                        css_template = file.read()

                    # Load the HTML template
                    html_template  = ""
                    html_file_path = None
                    # Depending on the type of analysis, load the approapiate template
                    #
                    # Numerical Univariate
                    if(self.type == "Numerical Univariate"):
                        html_file_path = constants.HTML_NUMERICAL_UNIVARIATE_TEMPLATE
                    # Numerical Categorical
                    elif(self.type == "Numerical Categorical"):
                        html_file_path = constants.HTML_NUMERICAL_CATEGORICAL_TEMPLATE
                    # Uknown type (error)
                    else:
                        print()
                        print(" I have no idea of the subtype of analysis we have")
                        print(" Type: ", self.type)
                        print()
                    
                    with open(html_file_path, 'r', encoding='utf-8') as file:
                        html_template = file.read()

                    # Insert the CSS code
                    html_template = html_template.replace('{{CSS_style}}', css_template)

                    # Values to insert
                    values = {
                        'folder_path':      self.folder_path,
                        'filename':         self.filename,
                        'type':             self.type,
                        'tablename':        self.tablename,
                        'lastUpdate_human': self.lastUpdate_human
                    }

                    # Replace placeholders
                    for key, value in values.items():
                        html_template = html_template.replace('{{' + key + '}}', str(value))

                    return(0, html_template)
                
            else:
                print("Can't save the analysis if you don't")
                print("save either the TXT or the HTML")
                print()
                print("Please set:")
                print(">>> myAnalysis.save(saveTXT  = True)")                
                print("or")
                print(">>> myAnalysis.save(saveHTML = True)")                
                print()

                return(-2,None)                
        else:
            print("I can't save the analysis if you don't give a folder path first")
            print("The current folder path is set to None.")
            print()
            print("Is not mandatory to have a folder defined,")
            print("You can still do the analysis and extract the information")
            print("But you can't save it into disk without a folder path")
            print()
            print("Notice that it protect you from saving the report accidentally")
            print("into the current woring directory by default")
            print("This can be annoying if you are doing 1000s of analysis in a loop,")
            print("which will end up with 1000s of accidental folders in your working directory")
            print()
            return(-1,None)
