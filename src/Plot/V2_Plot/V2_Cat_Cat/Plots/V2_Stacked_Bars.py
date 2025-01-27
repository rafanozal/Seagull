#!/usr/bin/env python3

# General libraries
import numpy as np
import matplotlib.pyplot      as plt
import matplotlib.ticker      as ticker
import matplotlib.patheffects as PathEffects

from scipy import stats

# Import the auxiliary libraries
import lib.color_manager as color_manager

# Import the main libraries
from ..V2_Cat_Cat import V2_Cat_Cat

class Barplot(V2_Cat_Cat):


    # Default constructor
    def __init__(self, data  = None, categorical_group_column = None, categorical_count_column = None,
                 folder_path = None,                                                                 # Rearranged parameters for easy use
                 extra_info:bool = True, rotate:bool = False, relative:bool = False,                 # Barplot parameters
                 top:int = 0 , order:str = "original",                                                  
                 fill_color_list_A = None, border_color_list_A     = None,                           # Barplot styles parameters
                 fill_alpha_list_A = None, border_thickness_list_A = None,              
                 fill_color_list_B = None, border_color_list_B     = None,                           
                 fill_alpha_list_B = None, border_thickness_list_B = None,              
                 **kwargs):                                                                          # Other parameters

        # -----------------------------------------
        # Do the parent constructor first
        # -----------------------------------------
        super().__init__(data                       = data,
                         categorical_column_A_index = categorical_group_column,
                         categorical_column_B_index = categorical_count_column,
                         folder_path                = folder_path,
                         **kwargs) # Pass common parameters to the parent constructor

        self.type        = "Stacked Barplot"
        self.relative    = relative
        self.data_name_y               = "Count"
        if(relative): self.data_name_y = "Frequency"

        # -----------------------------------------
        # Class attributes
        # -----------------------------------------
        
        # Python is shit man, it let you init variable whetever, that's why C++ is best and you won't have bugs related to that
        # it took me forever to find this bug and move this section to the start

        # Labels related
        self.extra_info     = extra_info  # If True, it will show the numeric values

        # Barplot related
        self.rotate         = rotate
        self.total_display  = self.data_A_length
        if(top > 0): self.total_display = min(top, self.data_A_length)
        self.order          = order

        # Style related (init to default if None is given)
        self.fill_color_list_A       = fill_color_list_A
        self.fill_alpha_list_A       = fill_alpha_list_A
        self.border_color_list_A     = border_color_list_A
        self.border_thickness_list_A = border_thickness_list_A
        self.fill_color_list_B       = fill_color_list_B
        self.fill_alpha_list_B       = fill_alpha_list_B
        self.border_color_list_B     = border_color_list_B
        self.border_thickness_list_B = border_thickness_list_B
        self.set_style()                                  

        # Update everything
        self.automatic_titles()
        self.automatic_size()
        self.automatic_filename()
        self.update_figure()

        

    # Automic figure size
    def automatic_size(self):

        # Automatic size is 1 base + 2 per category
        self.figure_width  = 1 + 2 * self.total_display
        self.figure_height = 5
        # Rotated if needed
        if(self.rotate):
            self.figure_width  = 5
            self.figure_height = 1 + 2 * self.total_display


    # Set the titles automatically based on the data
    # and if the user didn't set them manually before
    def automatic_titles(self):

        self.label_title    = "Stacked bars for "  + self.data_A_categorical_name + "(group) and " + self.data_B_categorical_name + "(count) in " + self.data_name
        self.label_subtitle = None
        self.label_x_axys   = ""
        self.label_y_axys   = self.data_name_y

    # Set the filename automatically for this type of plot
    def automatic_filename(self):

        # Init the strings for making the filename
        string_category_A = self.data_A_index
        string_category_B = self.data_B_index
        string_data_name  = self.data_name

        # Correct their values if needed
        # < 0 means the data was init randomly, hence no index
        string_category_A = None if string_category_A < 0 else str(string_category_A)
        string_category_B = None if string_category_B < 0 else str(string_category_B)

        # Put the strings together
        # If the strings are None, they won't be added to the filename
        join_indexes      = string_data_name
        string_indexes    = [string_category_A, string_category_B, string_data_name]
        filtered_indexes  = [s for s in string_indexes if s is not None]
        if len(filtered_indexes) > 1:
            join_indexes = '_'.join(filtered_indexes)

        # Set the final filename
        self.filename   = "Stacked_barplot_" + join_indexes

    # Switch showing extra data or not
    def show_extra_info(self, show = True):
        self.extra_info = show

    # Change how many bars are shown
    def set_top(self, top:int = 0):
        self.total_display = min(top, self.data_length)

    # Change the rotation of the plot
    def rotate(self):
        self.rotate = not(self.rotate)
    def set_horizontal(self):
        self.rotate = False
    def set_vertical(self):
        self.rotate = True

    # Set the style of the plot (evertything related to colors)
    # If set_defaults = True, it will assign None values to default
    # If set_defaults = False, it will keep the previous values
    def set_style(self, fill_color_list_A = None, border_color_list_A     = None,                  
                        fill_alpha_list_A = None, border_thickness_list_A = None,
                        fill_color_list_B = None, border_color_list_B     = None,                  
                        fill_alpha_list_B = None, border_thickness_list_B = None,                        
                        set_defaults = False):
 
        # ----------------
        #        A
        # ----------------
        # If the user gave a list of colors
        if(fill_color_list_A != None):
            
            # If the user gave a list of colors
            if(type(fill_color_list_A) == list):
                
                # Check that the list is the same length as the data
                if(len(fill_color_list_A) != self.data_A_length):
                    print()
                    print("WARNING!: The color list you gave me is not the same length as the data.")
                    print("          I will use the default colors instead.")
                    print()
                    
                    default_color        = color_manager.get_qualitative_colors(self.data_A_length)
                    self.fill_color_list = [default_color] * self.data_A_length
            
                # If everything is correct, use that color list
                else:
                    self.fill_color_list = fill_color_list_A

            # If the user gave a single color
            # We will use the same color for all the data
            else:
                self.fill_color_list = [fill_color_list_A] * self.data_A_length           

        # Otherwise, init to default
        else:
            if(set_defaults or self.fill_color_list_A == None):
                default_color        = color_manager.get_qualitative_colors(self.data_A_length)
                self.fill_color_list = [default_color] * self.data_A_length
        

        # If the user gave a list of border colors
        if(border_color_list_A != None):
            
            # If the user gave a list of colors
            if(type(border_color_list_A) == list):
                
                # Check that the list is the same length as the data
                if(len(border_color_list_A) != self.data_A_length):
                    print()
                    print("WARNING!: The border color list you gave me is not the same length as the data.")
                    print("          I will use the default border color instead.")
                    print()
                    
                    default_color        = "black"
                    self.fill_color_list = [default_color] * self.data_A_length
            
                # If everything is correct, use that color list
                else:
                    self.border_color_list = border_color_list_A

            # If the user gave a single color
            # We will use the same color for all the data
            else:
                self.border_color_list = [border_color_list_A] * self.data_A_length

        # Otherwise, init to default
        else:
            if(set_defaults or self.border_color_list == None):
                default_color          = "black"
                self.border_color_list = [default_color] * self.data_A_length


        # If the user gave a list of fill alphas
        if(fill_alpha_list_A != None):
            
            # If the user gave a list of colors
            if(type(fill_alpha_list_A) == list):
                
                # Check that the list is the same length as the data
                if(len(fill_alpha_list_A) != self.data_A_length):
                    print()
                    print("WARNING!: The fill alpha list you gave me is not the same length as the data.")
                    print("          I will use the default fill alpha instead.")
                    print()
                    
                    default_alpha        = 0.9
                    self.fill_alpha_list = [default_alpha] * self.data_A_length
            
                # If everything is correct, use that color list
                else:
                    self.fill_alpha_list = fill_alpha_list_A

            # If the user gave a single color
            # We will use the same color for all the data
            else:
                self.fill_alpha_list = [fill_alpha_list_A] * self.data_A_length   

        # Otherwise, init to default
        else:
            if(set_defaults or self.fill_alpha_list == None):
                default_alpha        = 0.9
                self.fill_alpha_list = [default_alpha] * self.data_A_length
     

        # If the user gave a list of border thickness
        if(border_thickness_list_A != None):
                
            # If the user gave a list of colors
            if(type(border_thickness_list_A) == list):
                
                # Check that the list is the same length as the data
                if(len(border_thickness_list_A) != self.data_A_length):
                    print()
                    print("WARNING!: The border thickness list you gave me is not the same length as the data.")
                    print("          I will use the default border thickness instead.")
                    print()
                    
                    default_thickness          = 1
                    self.border_thickness_list = [default_thickness] * self.data_A_length
            
                # If everything is correct, use that color list
                else:
                    self.border_thickness_list = border_thickness_list_A

            # If the user gave a single color
            # We will use the same color for all the data
            else:
                self.border_thickness_list = [border_thickness_list_A] * self.data_A_length

        # Otherwise, init to default
        else:
            if(set_defaults or self.border_thickness_list == None):
                default_thickness          = 1
                self.border_thickness_list = [default_thickness] * self.data_A_length


        # ----------------
        #        B
        # ----------------
        # If the user gave a list of colors
        if(fill_color_list_B != None):
            
            # If the user gave a list of colors
            if(type(fill_color_list_B) == list):
                
                # Check that the list is the same length as the data
                if(len(fill_color_list_B) != self.data_B_length):
                    print()
                    print("WARNING!: The color list you gave me is not the same length as the data.")
                    print("          I will use the default colors instead.")
                    print()
                    
                    default_color        = color_manager.get_qualitative_colors(self.data_B_length)
                    self.fill_color_list = [default_color] * self.data_B_length
            
                # If everything is correct, use that color list
                else:
                    self.fill_color_list = fill_color_list_B

            # If the user gave a single color
            # We will use the same color for all the data
            else:
                self.fill_color_list = [fill_color_list_B] * self.data_B_length           

        # Otherwise, init to default
        else:
            if(set_defaults or self.fill_color_list_B == None):
                default_color        = color_manager.get_qualitative_colors(self.data_B_length)
                self.fill_color_list = [default_color] * self.data_B_length
        

        # If the user gave a list of border colors
        if(border_color_list_B != None):
            
            # If the user gave a list of colors
            if(type(border_color_list_B) == list):
                
                # Check that the list is the same length as the data
                if(len(border_color_list_B) != self.data_B_length):
                    print()
                    print("WARNING!: The border color list you gave me is not the same length as the data.")
                    print("          I will use the default border color instead.")
                    print()
                    
                    default_color        = "black"
                    self.fill_color_list = [default_color] * self.data_B_length
            
                # If everything is correct, use that color list
                else:
                    self.border_color_list = border_color_list_B

            # If the user gave a single color
            # We will use the same color for all the data
            else:
                self.border_color_list = [border_color_list_B] * self.data_B_length

        # Otherwise, init to default
        else:
            if(set_defaults or self.border_color_list == None):
                default_color          = "black"
                self.border_color_list = [default_color] * self.data_B_length


        # If the user gave a list of fill alphas
        if(fill_alpha_list_B != None):
            
            # If the user gave a list of colors
            if(type(fill_alpha_list_B) == list):
                
                # Check that the list is the same length as the data
                if(len(fill_alpha_list_B) != self.data_B_length):
                    print()
                    print("WARNING!: The fill alpha list you gave me is not the same length as the data.")
                    print("          I will use the default fill alpha instead.")
                    print()
                    
                    default_alpha        = 0.9
                    self.fill_alpha_list = [default_alpha] * self.data_B_length
            
                # If everything is correct, use that color list
                else:
                    self.fill_alpha_list = fill_alpha_list_B

            # If the user gave a single color
            # We will use the same color for all the data
            else:
                self.fill_alpha_list = [fill_alpha_list_B] * self.data_B_length  

        # Otherwise, init to default
        else:
            if(set_defaults or self.fill_alpha_list == None):
                default_alpha        = 0.9
                self.fill_alpha_list = [default_alpha] * self.data_B_length
     

        # If the user gave a list of border thickness
        if(border_thickness_list_B != None):
                
            # If the user gave a list of colors
            if(type(border_thickness_list_B) == list):
                
                # Check that the list is the same length as the data
                if(len(border_thickness_list_B) != self.data_B_length):
                    print()
                    print("WARNING!: The border thickness list you gave me is not the same length as the data.")
                    print("          I will use the default border thickness instead.")
                    print()
                    
                    default_thickness          = 1
                    self.border_thickness_list = [default_thickness] * self.data_B_length
            
                # If everything is correct, use that color list
                else:
                    self.border_thickness_list = border_thickness_list_B

            # If the user gave a single color
            # We will use the same color for all the data
            else:
                self.border_thickness_list = [border_thickness_list_B] * self.data_B_length

        # Otherwise, init to default
        else:
            if(set_defaults or self.border_thickness_list == None):
                default_thickness          = 1
                self.border_thickness_list = [default_thickness] * self.data_B_length





    
    # Update the figure based on the data we have in the object
    def update_figure(self):

        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(self.figure_width, self.figure_height))

        # Create the data counting
        # (already done in the init of the plot)

        # Select the data that we will use
        final_categories = self.data_numerical_names
        final_counting   = self.data_count_list
        if(self.relative): final_counting = self.data_relative_list
        final_colors     = self.fill_color_list
        final_alphas     = self.fill_alpha_list
        final_borders    = self.border_color_list
        final_thickness  = self.border_thickness_list

        # Do whatever filtering needed

        # Make the plot
        for i in range(self.data_length):
            ax.bar(final_categories[i], final_counting[i], 
                   color = final_colors[i], 
                   alpha = final_alphas[i], 
                   edgecolor = final_borders[i], 
                   linewidth = final_thickness[i])


         # Add annotation to bars (if needed)
        if(self.extra_info):

            # Find the largest column
            largest_value = max(max(final_counting) , -min(final_counting))
            # Add as constant padding later
            padding_value = largest_value * 0.07

            # For each column
            for bar in ax.patches:

                # Get the width of the bar (positive or negative)
                bar_width  = bar.get_width()
                bar_height = bar.get_height()

                # Set the position of the text
                text_x = bar.get_x() + bar_width / 2  # Center of the bar
                text_y = 0

                # Set the position of the text depending on whether the bar is positive or negative
                if bar_height < 0:
                    # Place text above
                    text_y = bar_height + padding_value
                else:
                    # Place text bellow the bar
                    text_y = bar_height - padding_value

                # Display the text annotation                
                bars_labels = ax.text(text_x, text_y,
                                      f'{bar_height:.2f}' if self.relative else f'{bar_height:.0f}', 
                                      ha='center',  
                                      va='bottom' if bar_height < 0 else 'top', 
                                      fontsize=10, fontweight='bold',
                                      color='whitesmoke')

                
                # Add a black border around the text
                bars_labels.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='#343434')])

        



        # ---------------------------------------------------------------------
        # Plot theme:
        # ---------------------------------------------------------------------

        # Apply the theme for the plot
        ax.grid(color ='grey',
                linestyle ='-.', linewidth = 0.5,
                alpha = 0.2)
        
        # ---------------------------------------------------------------------
        # Plot labels:
        # ---------------------------------------------------------------------

        # Display the legend (no legend for univariates)
        # legend = ax.legend(title = self.data_categorical_name, loc = 'upper right')
        # legend._legend_box.align = "left"
        


        # Update and add Plot X and Y axys
        self.label_x_axys   = self.data_categorical_name
        self.label_y_axys   = self.data_name_y

        

        # Add Plot Title and subtitle
        total_padding = 0
        if(self.extra_info):           total_padding += 15
        if(self.label_subtitle!=None): total_padding += 15
        
        ax.set_title(self.label_title, loc = 'left', pad = total_padding)
        
        # Adding a subtitle using text
        if(self.label_subtitle!=None):
            ax.text(0, 1.1, self.label_subtitle, transform = ax.transAxes, ha = 'left', va = 'top', fontsize = 10, color = 'gray')

        ax.set_xlabel(self.label_x_axys)
        ax.set_ylabel(self.label_y_axys)

        # Uodate the figure internal object
        self.figure = fig
        self.axes   = ax