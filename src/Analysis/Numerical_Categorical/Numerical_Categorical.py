#!/usr/bin/env python3

'''
This file contain the implementation of the plot class: NUMERICAL_CATEGORICAL
'''

# General libraries
import numpy as np
import datetime

from scipy import stats

# Import the main libraries
from ..Analysis import Analysis
from ...Seagull import Seagull

# Constants
from src import constants


class Numerical_Categorical(Analysis):


    # Class specific imported methods
    from .methods.strings_representations import custom_str_method

    # Default constructor
    def __init__(self, folder_path = None, filename = "No_File_Name"):

        # -----------------------------------------
        # Do the parent constructor first
        # -----------------------------------------
        super().__init__(folder_path, filename)

        print(".####.")
        print(self.folder_path)

        # -----------------------------------------
        # Update the parent class attributes second
        # -----------------------------------------
        self.type          = "Numerical Categorical"

        # -----------------------------------------
        # Set the current class attributes last
        # -----------------------------------------

        # Subtype
        self.subtype:str          = "None"   # Short string with the subtype of analysis
        

        # Statistics
        self.pvalue:float        = 2.0
        self.pvalue_explain:str  = "None"   # Short string with the p-value interpretation
        self.test_method:str     = "None"   # Last time this was updated, was Student's or Welch’s
        self.variance_method:str = "None"   # Last time this was updated, was Bartlett or Levene

        # Group A Status
        self.group_a_name               = "Group A"
        self.group_a_sample             = 100
        self.group_a_normality          = False
        self.group_a_normality_pvalue   = 0
        self.group_a_normality_shapwilk = 0

        self.group_a_data               = np.random.rand(self.group_a_sample) 
        self.group_a_data               = (2 * self.group_a_data) - 1               

        # Group B Status
        self.group_b_name               = "Group B"
        self.group_b_sample             = 50
        self.group_b_normality          = False
        self.group_b_normality_pvalue   = 0
        self.group_b_normality_shapwilk = 0

        self.group_b_data               = np.random.rand(self.group_b_sample) 
        self.group_b_data               = (2 * self.group_b_data) - 1               

        # Both groups Status
        self.equal_variance_bartlett        = False
        self.equal_variance_bartlett_stat   = 0
        self.equal_variance_bartlett_pvalue = 2
        self.equal_variance_levene          = False
        self.equal_variance_levene_stat     = 0
        self.equal_variance_levene_pvalue   = 2

        # -----------------------------------------
        # Update the analysis
        # -----------------------------------------
        self.update()

    # -------------------------------------------------
    # Class methods:
    #     -__str__
    #     -__repr__
    #     -__len__
    #     -__iter__ (etc)
    # -------------------------------------------------
    # region

    # String
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


    # Do a simple parametric t-test    
    def get_parametric_pvalue(self, force = "none"):

        '''
        This function return the parametric p-value of two groups using Student
        or Welch automatically. No data transformation is used.

        The function returns the following data:

            p-value      (float): The p-value
            t-stat       (float): The original t-stat
            warning flag (bool):  False if no normallity condition was violated

        Algorithm:

            Check input flags:

                force = "none"    , skip this and select automatically.
                force = "auto"    , also skip the force, same as none.

                force = "student" , do Student's test regardless of any
                                    assuption. Will still flag the normality.
                force = "welch"   , Welch’s t-test regardless of any assuption.
                                    Will still flag the normality.

                force = "bartlett", does the option none forcing barlett test,
                                    which already does by default. This option
                                    is only here for anyone that likes to write
                                    it explicetelly in the code.

                force = "levene"  , does the option none forcing Levene's test.
                

            Check for normality:

                Either group is not normal:

                    If either group of data is not normally distributed, it
                    flag the results with a warning and performs a Welch’s
                    t-test by default anyway.

                    If force = "student" is set, will do a Student's test
                    instead automatically. The flag will also be active.

                    The function get_non_parametric_pvalue() can be use as
                    alternative in this scenario.

                Both groups are normal:

                    Check for Equal Variances (Bartlett’s Test):

                    Since we have established that both groups are normally
                    distributed, using Bartlett’s test is appropriate because
                    it is more powerful under the assumption of normality.

                    However, it's worth noting that Bartlett's test can still
                    be sensitive to deviations from normality that might not be
                    detected by your normality test, depending on sample size
                    and the test's power.

                    While Levene's test is indeed robust to deviations
                    from normality, it can still be used even when data is
                    normal. It is less sensitive to outliers than Bartlett’s
                    test and can provide a "safer" option if there's any
                    uncertainty about the robustness of the normality
                    assumption (e.g., borderline cases in normality testing).
                    This can be done by setting force = "levene" in the
                    parameters.

                        If variance is similar, do a Student's test

                        If variance is not similar, do a Welch’s test

        Statistical Background:

            Student’s t-test: Assumes that the two distributions have the same
            variance. The formula for the test statistic involves the pooled
            variance of the two samples.

            Welch’s t-test: Does not assume equal population variance and
            adjusts the degrees of freedom used in the hypothesis test to
            account for this. This test is more appropriate for cases where the
            sample sizes and variances are unequal between the two groups,
            providing a more accurate approximation of the degrees of freedom.

            Levene's Test: Levene's test is more robust to departures from
            normality than Bartlett's test. It tests the null hypothesis that
            all input samples are from populations with equal variances. 

            Bartlett's Test: tests the null hypothesis that all input samples
            are from populations with equal variances. It is sensitive to
            departures from normality.         
        '''
        # Prepare the results
        final_p_value        = 2
        final_t_stat         = 1023
        warning_no_normality = False

        # Calculate normality
        self.group_a_normality, self.group_a_normality_pvalue, self.group_a_normality_shapwilk = Analysis.normality(self.group_a_data)
        self.group_b_normality, self.group_b_normality_pvalue, self.group_b_normality_shapwilk = Analysis.normality(self.group_b_data)

        # Calculate variance
        self.equal_variance_levene_stat,   self.equal_variance_levene_pvalue   = stats.levene(self.group_a_data, self.group_b_data)
        self.equal_variance_bartlett_stat, self.equal_variance_bartlett_pvalue = stats.bartlett(self.group_a_data, self.group_b_data)

        self.equal_variance_levene   = self.equal_variance_levene_pvalue   >= 0.05
        self.equal_variance_bartlett = self.equal_variance_bartlett_pvalue >= 0.05
        

        # Check for normality
        warning_no_normality = not(self.group_a_normality and self.group_b_normality)
        
        # Check for variance
        equal_variance       = self.equal_variance_bartlett
        self.variance_method = "bartlett"
        if(force == "levene"):
            equal_variance       = self.equal_variance_levene
            self.variance_method = "levene"

        # Check the users's flags
        if(force == "student" or equal_variance):
            final_t_stat, final_p_value = stats.ttest_ind(self.group_a_data, self.group_b_data, equal_var = True)
            self.test_method = "student"
        else:
            final_t_stat, final_p_value = stats.ttest_ind(self.group_a_data, self.group_b_data, equal_var = False)
            self.test_method = "welch"

        # Update object
        self.pvalue           = final_p_value
        self.lastUpdate       = datetime.datetime.now()
        self.lastUpdate_human = self.lastUpdate.strftime("%Y-%m-%d %H:%M:%S")
        self.subtype          = "Parametric T-test"

        # Return the results
        return [final_p_value, final_t_stat, warning_no_normality]


    # Update the analysis
    def update(self):
        self.get_parametric_pvalue()

    # ----------------------------------
    # Saving the analysis in disk
    # ----------------------------------
    def save(self, saveTXT = True, saveHTML = True):

        # Get the parent result
        error, Analysis_HTML = super().save(saveTXT, saveHTML)
        
        if(error >= 0):

            # Values to insert
            values = {

                'subtype':     self.subtype,
                'pvalue':      self.pvalue,
                'pasterisk':   self.p_value_to_significance(self.pvalue),
                'test_method': self.test_method,


                'normality_check':             constants.EMOJI_CHECK_CORRECT,
                'group_a_normality_pasterisk': self.p_value_to_significance(self.group_a_normality_pvalue),
                'group_a_normality_pvalue':    self.group_a_normality_pvalue,
                'group_a_normality_shapwilk':  self.group_a_normality_shapwilk,
                'group_a_check':               constants.EMOJI_CHECK_CORRECT,
                'group_b_normality_pasterisk': self.p_value_to_significance(self.group_b_normality_pvalue),
                'group_b_normality_pvalue':    self.group_b_normality_pvalue,
                'group_b_normality_shapwilk':  self.group_b_normality_shapwilk,
                'group_b_check':               constants.EMOJI_CHECK_CORRECT,

                'group_a_name':   self.group_a_name,
                'group_a_sample': self.group_a_sample,
                'group_a_data':   self.group_a_data,
                'group_b_name':   self.group_a_name,
                'group_b_sample': self.group_b_sample,
                'group_b_data':   self.group_b_data,

                'variance_check':                    constants.EMOJI_CHECK_CORRECT,
                'bartlett_check':                    constants.EMOJI_CHECK_CORRECT,
                'levene_check':                      constants.EMOJI_CHECK_CORRECT,
                'variance_method':                   self.variance_method,
                'equal_variance_bartlett_pasterisk': self.p_value_to_significance(self.equal_variance_bartlett_pvalue),
                'equal_variance_bartlett_pvalue':    self.equal_variance_bartlett_pvalue,
                'equal_variance_bartlett_stat':      self.equal_variance_bartlett_stat,
                'equal_variance_levene_pasterisk':   self.p_value_to_significance(self.equal_variance_levene_pvalue),
                'equal_variance_levene_pvalue':      self.equal_variance_levene_pvalue,
                'equal_variance_levene_stat':        self.equal_variance_levene_stat,

            }
            # Correct conditional values
            if(self.group_a_normality_pvalue>0.05):
                values['group_a_check']   = constants.EMOJI_CHECK_FAIL
                values['normality_check'] = constants.EMOJI_CHECK_FAIL
                
            if(self.group_b_normality_pvalue>0.05):
                values['group_b_check']   = constants.EMOJI_CHECK_FAIL
                values['normality_check'] = constants.EMOJI_CHECK_FAIL

            if(self.variance_method == 'bartlett'):
                if(self.equal_variance_bartlett_pvalue < 0.05):
                    values['variance_check'] = constants.EMOJI_CHECK_FAIL
                    values['bartlett_check'] = constants.EMOJI_CHECK_FAIL
            else:
                if(self.equal_variance_levene_pvalue < 0.05):
                    values['variance_check'] = constants.EMOJI_CHECK_FAIL
                    values['levene_check']   = constants.EMOJI_CHECK_FAIL

            # Replace placeholders
            for key, value in values.items():
                Analysis_HTML = Analysis_HTML.replace('{{' + key + '}}', str(value))

            # Save to file
            save_path = self.folder_path + "/" + self.filename + ".html"
            with open(save_path, 'w') as file:
                file.write(Analysis_HTML)

            return(0, Analysis_HTML)

