import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import random

def get_colors(colormap_name, total):
    """
    Returns a list of colors from the specified Matplotlib colormap equally spaced.
    
    Args:
    colormap_name (str): Name of the colormap (e.g., 'RdBu').
    total (int): Total number of colors to return.
    
    Returns:
    list [string]: A list of colors in HEX code format.
    """
    cmap = plt.get_cmap(colormap_name)  # Get the colormap
    colors = cmap(np.linspace(0, 1, total))  # Generate colors from the colormap
    hex_colors = [matplotlib.colors.rgb2hex(color[:3]) for color in colors]  # Convert to hexadecimal
    return hex_colors


def generate_random_colors(total):
    """
    Generate a list of random colors in HEX code format.

    Parameters:
    total (int): Total number of colors to return.

    Returns:
    list [string]: A list of strings representing the colors in HEX code format.
    """
    colors = []
    for _ in range(total):
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        colors.append(color)
    return colors


def color_to_hex(color_name):
    """
    Converts a named Matplotlib color to its hexadecimal equivalent.

    Args:
    color_name (str): The name of the color (e.g., 'dimgrey').

    Returns:
    str: The hexadecimal representation of the color.
    """
    # Get the RGB equivalent of the named color
    rgb = mcolors.to_rgb(color_name)
    # Convert RGB to hexadecimal
    hex_color = mcolors.to_hex(rgb)
    return hex_color



# Examples usage:
def main():

    colors = get_colors('RdBu', 3)
    print(colors)                         # Output should include red-ish, white, and blue-ish in hexadecimal
    colors = generate_random_colors(3)
    print(colors)
    hex_color = color_to_hex('dimgrey')
    print(hex_color)

# Call the main function
if __name__ == "__main__":
    main()