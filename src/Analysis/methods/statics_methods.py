from scipy import stats


NORMAL_DISTRIBUTIONS = ['norm', 'normal', 'Normal', 'NORMAL', 'Norm', 'NORM']

# For a given distribution type, find out if there's a scipy valid equivalent
#
# Return the equivalent scipy distribution type
#        None if the given distribution type is not valid
def get_distribution_type(distribution_type):

    target_distribution = None

    # Find out which ditribution we are using
    if(distribution_type in NORMAL_DISTRIBUTIONS):
        target_distribution = 'norm'
    elif(distribution_type == "exponential"):
        target_distribution = 'expon'
    elif(distribution_type == "uniform"):
        target_distribution = 'uniform'
    else:
        print()
        print("ERROR!: The given distribution: " + str(distribution_type) + " is not valid.")
        print("        The test haven't been performed.")
        print()
        print("        I can use any of these:")
        print()
        print("        - Normal Distributions: " + str(NORMAL_DISTRIBUTIONS) )
        print()

    return target_distribution



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
def normality(numerical_data, significance_level = 0.05):
    '''
    Shapiro-Wilk Test

    The Shapiro-Wilk test is widely used for testing the normality of data.
    It tests the null hypothesis that the data was drawn from a normal
    distribution.

    Return:
    
        True, if normally distributed. False otherwise
        p-value of the test
        test statistic
    '''
    stat_normal, p_value_normal = stats.shapiro(numerical_data)

    return [p_value_normal > significance_level, p_value_normal, stat_normal]


# Kolmogorov-Smirnov Test (K-S Test)
#
# Description: The K-S test measures the maximum distance between the empirical distribution function of the sample data and the cumulative distribution function (CDF) of the specified theoretical distribution.
# Application: It can be used for any continuous distribution and is non-parametric.
#
# Results
#     - p-value: The probability that the sample data was drawn from the specified distribution.
#                If the p-value is less than the significance level (e.g., 0.05), the given data is NOT of the given distribution.
#     - Statistic: The maximum distance between the empirical distribution and the CDF.
@staticmethod
def kolmogorov_smirnov(numerical_data, distribution_type, significance_level = 0.05):

    test_results = False
    statistic    = -1
    p_value      = -1

    target_distribution = get_distribution_type(distribution_type)

    # If we found a valid distribution option, do the test
    if(target_distribution != None):
        statistic, p_value = stats.kstest(numerical_data, target_distribution)
        test_results = p_value > significance_level

    # Return the results
    return [test_results, p_value, statistic]

# Anderson-Darling Test
#
# Description: This test gives more weight to the tails than the K-S test. It is a measure of the distance between the sample distribution and the specified theoretical distribution.
# Application: Particularly sensitive to deviations in the tail, which makes it very useful for distributions where tail behavior is important.
#
# Results
#     - p-value: The probability that the sample data was drawn from the specified distribution.
#                If the p-value is less than the significance level (e.g., 0.05), the given data is NOT of the given distribution.
#     - Statistic: The maximum distance between the empirical distribution and the CDF.


@staticmethod
def anderson_darling(numerical_data, distribution_type):

    statistic = -1
    p_values  = None

    target_distribution = get_distribution_type(distribution_type)

    # If we found a valid distribution option, do the test
    if(target_distribution != None):
        # Perform the Anderson-Darling test for whatever distribution
        result = stats.anderson(numerical_data, target_distribution)

        # There's only one statistic for the Anderson Darling test
        statistic = result.statistic

        # Create a list of triplets:
        #     - significance level (15%, 10%, ...)
        #     - critical value
        #     - Whether the data looks like the distribution or not (default is False)
        p_values = list(zip(result.significance_level, result.critical_values, [False]*len(result.critical_values)))

        # Each critical value needs to compared with the statistic
        # If the statistic is less than the critical value, the data looks like whatever distribution (True)
        # Otherwise, the data does not look like whatever distribution (False, Default)

        # The critical values and corresponding significance levels
        for i in range(len(result.critical_values)):
            cv = result.critical_values[i]
            if result.statistic < cv:
                p_values[i][2] = True
                
    # Return the results
    return [p_values, statistic]