import re # Regular expressions

def find_matches_in_list(string_list, value):
    """
    Returns a list of booleans indicating whether each element in 'string_list' matches 'value'.
    
    Args:
    string_list (list of str): The list of strings to search.
    value (str): The string value to find in the list.
    
    Returns:
    list of bool: A list where each element is True if the corresponding element in 'string_list' matches 'value', otherwise False.
    """
    # Initialize a boolean list with False values
    match_list = [False] * len(string_list)
    
    # Iterate over the string list and update the boolean list
    for index, item in enumerate(string_list):
        if item == value:
            match_list[index] = True
    
    return match_list


def find_position_in_list(string_list, value):
    """
    Returns the index of 'value' in 'string_list' if it exists, otherwise returns -1.
    
    Args:
    string_list (list of str): The list of strings to search.
    value (str): The string value to find in the list.
    
    Returns:
    int: The index of the value if it exists, -1 otherwise.
    """
    index = 0
    found = False
    list_length = len(string_list)  # Get the length of the list to avoid going out of bounds

    while index < list_length and not found:
        if string_list[index] == value:
            found = True  # Set found to True if the value is found
        else:
            index += 1  # Increment index if not found

    # Return the result
    if (found == False): index = -1
    return index

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

def clean_weird_characters(weird_string:str) -> str:
    """
    Delete the strange characters from a string and transform the result into
    an ISO_8859-2 encoded string. White spaces are transformed into "_"
    characters instead.
    
    This is intended to use to clean filenames and filepath incompatible
    characters.
    
    param:
        weird_string: The string that you want to clean

    return:
        a new string with the weirdness removed

    example:

        clean_weird_characters("This(is),a, very$$ weird$:String")
         > "Thisisa_very_weirdString"
    """

    # Replace specific weird characters with nothing
    weird_string = re.sub(r"[:\$%'\"<>\[\]()/\\]", "", weird_string)
    
    # Replace spaces with underscores
    weird_string = re.sub(r" ", "_", weird_string)
    
    # Convert to ISO_8859-2 encoding if necessary
    # Note: Python internally uses Unicode, and encoding to bytes might not be needed unless for specific I/O operations
    # weird_string = weird_string.encode('iso-8859-2').decode('iso-8859-2')
    
    return weird_string