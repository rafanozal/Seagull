#!/usr/bin/env python3

'''
This file contain the implementation of the plot class: NUMERICAL_UNIVARIATE


1. Descriptive Statistics

    Mean, Median, Mode: Measures of central tendency that summarize the average and most frequent values in your dataset.
    Standard Deviation and Variance: Measures of dispersion that describe the spread of the data around the mean.
    Range, Minimum, Maximum: Provide insights into the span of the data.
    Quantiles (including Quartiles): Divide the data into equal parts, which can help in understanding the distribution.

2. Visualization Techniques

    Histogram: Visual representation of the distribution of the numerical data, showing the frequency of data intervals.
    Density Plot: Smoothed version of the histogram, often used to see the shape of the distribution more clearly.
    (Box Plot: Not much sense if you have the density plot)

3. Normality Tests

    Shapiro-Wilk Test: Tests the hypothesis that the data was drawn from a normally distributed population.
    Anderson-Darling Test: A more powerful test compared to the Shapiro-Wilk test, focusing on the tails of the distribution.
    Kolmogorov-Smirnov Test: Compares the empirical distribution of the data with a specified distribution (e.g., normal distribution).

4. Goodness-of-Fit Tests

    Chi-Squared Goodness-of-Fit Test: Tests whether the sample data matches a population with a specific distribution.
    K-S Test for Goodness-of-Fit: Can be used to compare the sample data with a continuous distribution to see how well it fits.

    
        1. Normal Distribution (Gaussian Distribution)

            Characteristics: Symmetric, bell-shaped curve; defined by two parameters: mean (μ) and standard deviation (σ).
            Applications: Suitable for many natural phenomena and measurement errors.

        2. Uniform Distribution

            Characteristics: Equal probability for all values within a specific interval [a, b]; zero probability outside this interval.
            Applications: Ideal for representing an idealized random process where each outcome is equally likely.

        3. Exponential Distribution

            Characteristics: Describes the time between events in a Poisson point process; characterized by a rate parameter (λ).
            Applications: Commonly used to model waiting times or the time until a specific event (e.g., failure of a component).

        4. Poisson Distribution

            Characteristics: Probability distribution of a number of events occurring in a fixed interval of time or space, given the average number of times the event occurs over that interval.
            Applications: Useful for modeling count data, such as the number of emails received in an hour.

        5. Binomial Distribution

            Characteristics: Describes the number of successes in a fixed number of independent Bernoulli trials, each with the same probability of success.
            Applications: Often used in quality control, survey analysis, and other scenarios with binary outcomes.

        6. Weibull Distribution

            Characteristics: Flexible distribution characterized by a shape parameter (k) and a scale parameter (λ); can model various types of distributions depending on k.
            Applications: Widely used in reliability engineering and survival analysis.

        7. Log-Normal Distribution

            Characteristics: If the logarithm of the variable is normally distributed, then the variable itself has a log-normal distribution.
            Applications: Commonly used to model stock prices, lifetimes of units whose failure modes are of a fatigue-stress nature, and other data that grow exponentially.

        8. Gamma Distribution

            Characteristics: Two-parameter family of continuous probability distributions with a shape parameter (k) and a scale parameter (θ).
            Applications: Useful in modeling waiting times for multiple events (like the exponential distribution for a single event).

        9. Beta Distribution

            Characteristics: Defined on the interval [0, 1] and characterized by two shape parameters, α and β, which determine the shape of the distribution.
            Applications: Useful in modeling phenomena which are limited to a range between 0 and 1, such as probabilities and proportions.

        10. Chi-Squared Distribution

            Characteristics: The distribution of a sum of the squares of k independent standard normal random variables.
            Applications: Commonly used in hypothesis testing and confidence interval estimation for variance in the normal distribution.



5. Parameter Estimation

    Fit Distribution Parameters: Estimate the parameters of a theoretical distribution that best fits your data. Common distributions include normal, exponential, log-normal, etc.
        Software packages like R, Python (SciPy library), or specialized statistical software can be used to fit distributions and estimate parameters.

6. Outlier Detection

    Z-Score Analysis: Identifies outliers by measuring the distance (in standard deviations) of a data point from the mean.
    IQR Method: Uses the interquartile range to find data points that are too far from the central values.



'''

# General libraries
import numpy as np
import datetime

from scipy import stats

# Import auxiliary libraries
import lib.solvers as my_solvers

# Import the main libraries
from ..Analysis import Analysis
from ...Plot.V1_Plot.V1Numerical.V1_Density import Density_plot

#from ...Seagull import Seagull

# Constants
from src import constants


class Numerical_Univariate(Analysis):


    # Class specific imported methods
    from .methods.strings_representations import custom_str_method

      # Imported methods
    # ---- Setters and getters
    from .methods.setters_getters import (
        get_data_name, get_data_name_x
    )



    # Default constructor
    def __init__(self, data = None, numerical_column_index:int = None, folder_path = None, # Rearranged parameters for easy use
                 column:str = None,                                                        # Alias for numerical_column_index
                 filename   = None,                                                        # Numerical analysis parameters
                **kwargs):                                                                 # Other parameters
        
        
        # -----------------------------------------
        # Data related
        # -----------------------------------------
        self.invalid_data_index = True # Assume the index is invalid until proven otherwise
        self.data_x:np.array    = None
        self.data_name:str      = None
        self.data_name_x:str    = None

        # -----------------------------------------
        # Do the parent constructor first
        # -----------------------------------------
        super().__init__(folder_path = folder_path, filename = filename, **kwargs)  # Pass common parameters to the parent constructor

        # -----------------------------------------
        # Update the parent class attributes second
        # -----------------------------------------
        self.type:str = "Numerical Univariate"
        

        # -----------------------------------------
        # Start the actual constructor
        # -----------------------------------------
        
        solved_parameters = my_solvers.solve_source_data(data, numerical_column_index, column, constants.NUMERICAL_TYPES)

        # Check that the solution is valid
        #
        #     - If a seagull or pandas, with index > 0, and the data is as expected
        #     - If numpy array and the data is as expected
        #
        # Otherwise default to random data

        if(not((solved_parameters[0] == "Seagull" and solved_parameters[1] > 0 and solved_parameters[2] == True) or \
               (solved_parameters[0] == "Pandas"  and solved_parameters[1] > 0 and solved_parameters[2] == True) or \
               (solved_parameters[0] == "Numpy"                                and solved_parameters[2] == True))):
            
            print()
            print("WARNING!: The data you gave me is not valid.")
            print("          I will use random data instead.")

            solved_parameters = [None, -1, False]
        

        # If the user gave no data or unknown data, use random data
        if(solved_parameters[1] == "Uknown"):

            print()
            print("WARNING!: I don't understand the data you gave me.")
            print("          I will use random data instead.")
            print()

        if(solved_parameters[0] == None or solved_parameters[1] == "Uknown"):

            self.data_x = np.sort(np.random.rand(100)) # Initialize a random array
            self.data_x = (2 * self.data_x) - 1          # Scale between -1 and 1
            self.data_name   = "Random Data"
            self.data_name_x = "X"      

        # If the user gave a Seagull object
        if(solved_parameters[0] == "Seagull"):

            self.data_x      = data.get_column_values(solved_parameters[1])
            self.data_name   = data.get_name()
            self.data_name_x = data.get_column_name(solved_parameters[1])

        # If the user gave a pandas dataframe
        if(solved_parameters[0] == "Pandas"):

            self.data_x      = data.iloc[ :  , solved_parameters[1]].to_numpy()
            self.data_name   = data.name
            self.data_name_x = data.columns[solved_parameters[1]]

        # If the user gave a numpy array
        if(solved_parameters[0] == "Numpy"):

            self.data_x      = data
            self.data_name   = None
            self.data_name_x = None

        
        # -----------------------------------------
        # Set the current class attributes to defaults
        # -----------------------------------------

        # Subtype
        self.subtype:str  = "None"   # Univaraite analysis don't have any subtypes
        
        # Descriptive statistics
        self.sample_size  = 0

        self.p05:float    = 0
        self.p25:float    = 0
        self.median:float = 0
        self.p75:float    = 0
        self.p95:float    = 0

        self.mean:float   = 0
        self.std:float    = 0
        self.var:float    = 0

        self.range:float  = 0
        self.iqr:float    = 0
        self.min:float    = 0
        self.max:float    = 0

        # Plots
        self.histogram    = None
        self.density      = None
        
        # Distributions fits
        #     Normal
        self.normal_fit_shapiro    = None
        self.normal_fit_mu         = None
        self.normal_fit_sigma      = None
        self.normal_fit_kolmogorov = None
        self.normal_fit_anderson   = None




        self.uniform_fit     = None
        self.exponential_fit = None
        self.poisson_fit     = None
        self.binomial_fit    = None
        self.weibull_fit     = None
        self.lognormal_fit   = None
        self.gamma_fit       = None
        self.beta_fit        = None
        self.chisquared_fit  = None

        # -----------------------------------------
        # Update the analysis and find all the statistics
        # -----------------------------------------
        self.update()

        # -----------------------------------------
        # Update some names that might be empty
        # -----------------------------------------
        if(self.filename    == None): self.filename  = "Numerical_Univariate_Analysis_" + str(self.lastUpdate)
        if(self.data_name   == None): self.data_name = "Uknown data origin"
        if(self.data_name_x == None): self.data_name = "X"

        # -----------------------------------------
        # Update the plots
        # -----------------------------------------
        
        
        
        

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

    # endregion


    # Update the analysis
    def update(self):

        self.sample_size  = len(self.data_x)

        # Descriptive statistics

        percentiles = np.percentile(self.data_x, [5, 25, 50, 75, 95])

        self.p05:float    = percentiles[0]
        self.p25:float    = percentiles[1]
        self.median:float = percentiles[2]
        self.p75:float    = percentiles[3]
        self.p95:float    = percentiles[4]

        self.mean:float   = np.mean(self.data_x)
        self.std:float    = np.std(self.data_x)
        self.var:float    = np.var(self.data_x)

        self.range:float  = np.max(self.data_x) - np.min(self.data_x)
        self.iqr:float    = self.p75 - self.p25
        self.min:float    = np.min(self.data_x)
        self.max:float    = np.max(self.data_x)

        # Plots
        self.histogram    = None
        self.density      = None

        # If we have a place where to save the plot
        if(self.folder_path != None):        

            # Init the density plot with the current data information
            self.density = Density_plot()
            self.density.set_folder_path(self.folder_path)
            self.density.set_filename("main_density_plot")
            self.density.set_data_x(self.data_x)
            self.density.set_data_name(self.data_name)
            self.density.set_data_name_x(self.data_name_x)
            self.density.set_title("")
            self.density.set_subtitle("")
            self.density.save()
            

        # Distributions fits
        #
        #     Normal
        #
        self.normal_fit_mu         = self.mean
        self.normal_fit_sigma      = self.std
        self.normal_fit_shapiro    = Analysis.normality(self.data_x)
        self.normal_fit_kolmogorov = Analysis.kolmogorov_smirnov(self.data_x, 'norm')
        self.normal_fit_anderson   = Analysis.anderson_darling(self.data_x, 'norm')



        self.uniform_fit     = None
        self.exponential_fit = None
        self.poisson_fit     = None
        self.binomial_fit    = None
        self.weibull_fit     = None
        self.lognormal_fit   = None
        self.gamma_fit       = None
        self.beta_fit        = None
        self.chisquared_fit  = None

        # Update the last update variables
        self.lastUpdate       = datetime.datetime.now()
        self.lastUpdate_human = self.lastUpdate.strftime("%Y-%m-%d %H:%M:%S")

    # ----------------------------------
    # Saving the analysis in disk
    # ----------------------------------
    def save(self, saveTXT = True, saveHTML = True):

        # Get the parent result
        error, Analysis_HTML = super().save(saveTXT, saveHTML)
        
        if(error >= 0):

            # Values to insert
            values = {

                'data_x_name': self.data_name_x,
                'sample_size': self.sample_size,
                #'data_x':      self.data_x,

                'min':         round(self.min,2),
                'p05':         round(self.p05,2),
                'p25':         round(self.p25,2),
                'median':      round(self.median,2),
                'p75':         round(self.p75,2),
                'p95':         round(self.p95,2),
                'max':         round(self.max,2),

            }


            # Replace placeholders
            for key, value in values.items():
                Analysis_HTML = Analysis_HTML.replace('{{' + key + '}}', str(value))

            # Save to file
            save_path = self.folder_path + "/" + self.filename + ".html"
            with open(save_path, 'w') as file:
                file.write(Analysis_HTML)

            return(0, Analysis_HTML)

