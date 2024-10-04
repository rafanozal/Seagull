from scipy import stats

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