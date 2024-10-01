# General libraries
import numpy  as np
import pandas as pd
import random

from scipy import stats

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
    #
    # ---- String representations
    #      
    #      Showing the data in different ways at the console. Useful for debugging and quick overview.
    from .methods.strings_representations import external_str_method

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------

    def __init__(self, folder_path = None, filename = "No_File_Name"):
        
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
        
        print("···")
        print(self.folder_path)

        if(self.folder_path != None):

            print("Saving...")
            print(self.folder_path + "/" + self.filename)

        else:
            print("Can't save the analysis if you don't give a folder path first")
            print()
            print("Is not mandatory to have a folder defined!")
            print()
            print("it protect you from saving the report accidentally")
            print("Which can be annoying if you are doing 1000s of analysis in a loop")



    # -------------------------------------------------
    # Others
    # 
    #     - Common methods to many subclasses
    # -------------------------------------------------

    # Transform p-values into asterisks
    @staticmethod
    def p_value_to_significance(p_value):
        """
        Transforms a p-value into a significance level string based on conventional statistical thresholds.

        Parameters:
        - p_value (float): A numerical p-value between 0 and 1, typically obtained from statistical tests.

        Returns:
        - str: A string representing the significance level:
            "****" for p < 0.0001 (highly significant),
            "***"  for p < 0.001  ,
            "**"   for p < 0.01   ,
            "*"    for p < 0.05   ,
            "ns"   for p >= 0.05  (not significant).

        Examples:
        >>> p_value_to_significance(0.00005)
        '****'
        >>> p_value_to_significance(0.004)
        '***'
        >>> p_value_to_significance(0.03)
        '*'
        >>> p_value_to_significance(0.1)
        'ns'
        """
        if p_value < 0.0001:
            return '****'
        elif p_value < 0.001:
            return '***'
        elif p_value < 0.01:
            return '**'
        elif p_value < 0.05:
            return '*'
        else:
            return 'ns'

    # Check whether data is normally distributed or not based on Shapiro-Wilk test
    @staticmethod
    def normality(numerical_data):
        '''
        Shapiro-Wilk Test

        The Shapiro-Wilk test is widely used for testing the normality of data.
        It tests the null hypothesis that the data was drawn from a normal
        distribution.

        Return True if normally distributed
        '''
        stat_normal, p_value_normal = stats.shapiro(numerical_data)

        return [p_value_normal<0.05, p_value_normal, stat_normal]
