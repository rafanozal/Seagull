

def robust_int_conversion(number_str):
    """
    Converts a string to an integer, removing commas if present.
    
    Args:
    number_str (str): The string representation of the number, which may include commas.
    
    Returns:
    int: The integer value of the number.
    
    Raises:
    ValueError: If the input is not a valid integer.
    """

    if(type(number_str) == str):
        # Remove commas if present
        number_str = number_str.replace(',', '')
        number_str = int(number_str)
    
    # Convert to integer
    return number_str