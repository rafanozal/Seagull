import random
import string

# Set the whole dataset to float zeros
def zero(self):

    float_zero  = 0.0
    int_zero    = 0
    string_zero = '0'

    for j in range(self.totalColumns):

        # Get the column type
        column_type = self.data.iloc[:,j].dtype

        for i in range(self.totalRows):
        
            # Strings
            if(column_type == "object"):
                self[i,j] = string_zero
            elif(column_type == "category"):
                self[i,j] = string_zero

            # Floats
            if(column_type == "float32"):
                self[i,j] = float_zero
            elif(column_type == "Float32"):    
                self[i,j] = float_zero         
            if(column_type == "float64"):
                self[i,j] = float_zero
            elif(column_type == "Float64"):    
                self[i,j] = float_zero

            # Integers
            if(column_type == "int64"):
                self[i,j] = int_zero
            elif(column_type == "int32"):
                self[i,j] = int_zero
            elif(column_type == "Int64"):
                self[i,j] = int_zero
            elif(column_type == "Int32"):
                self[i,j] = int_zero                                  

            # Dates

            # Default
            else:
                self[i,j] = string_zero

# Fill the DF with random float data
def randomize(self, string_length = 10,
              int_min = -10 ,  int_max = 10,
              float_min = -1 , float_max = 1,
              date_min = "1970-01-01", date_max = "3000-12-31"):

    from ...Seagull import Seagull

    for j in range(self.totalColumns):

        # Get the column type
        column_type = self.data.iloc[:,j].dtype

        for i in range(self.totalRows):

            # Strings
            if(column_type == "object"):
                self[i,j] = ''.join(random.choices(string.ascii_lowercase, k = string_length))
            elif(column_type == "category"):
                self[i,j] = ''.join(random.choices(string.ascii_lowercase, k = string_length))

            # Dates
            elif(column_type == "date"):
                self[i,j] = Seagull.generate_random_date(date_min,date_max)
            elif(column_type == "datetime64[ns]"):
                self[i,j] = Seagull.generate_random_date(date_min,date_max)
                
            # Floats
            elif(column_type == "float32"):
                self[i,j] = random.uniform(float_min, float_max)
            elif(column_type == "Float32"):    
                self[i,j] = random.uniform(float_min, float_max)
            elif(column_type == "float64"):
                self[i,j] = random.uniform(float_min, float_max)
            elif(column_type == "Float64"):    
                self[i,j] = random.uniform(float_min, float_max)

            # Integers
            elif(column_type == "int64"):
                self[i,j] = random.randint(int_min, int_max)
            elif(column_type == "int32"):
                self[i,j] = random.randint(int_min, int_max)
            elif(column_type == "Int64"):
                self[i,j] = random.randint(int_min, int_max)
            elif(column_type == "Int32"):
                self[i,j] = random.randint(int_min, int_max)                                  

            # Default (strings)
            else:
                self[i,j] = ''.join(random.choices(string.ascii_lowercase, k = string_length))


# Randomize the whole dataset to categorical data
# Number of categories optional
def randomize_categorical(self, total_categories = 5, string_length = 10):

    # Initialize the categories at random
    my_random_categories = ["Random"] * total_categories
    for i in range(len(my_random_categories)):

        current_random = ''.join(random.choices(string.ascii_lowercase, k = string_length))
        my_random_categories[i] = current_random
        
    # Assign the random values to random cells
    for i in range(self.totalRows):
        for j in range(self.totalColumns):

            self[i,j] = random.choice(my_random_categories)

    # Convert all columns into proper categorical
    # Use the sorting of whatever original first random order had
    for j in range(self.totalColumns):
        self.column_to_category(j, categoryList = my_random_categories)

    # Update the info in the internal object
    self.types    = ["categorical"] * self.totalColumns
    self.totalNAs = [0]             * self.totalColumns  





# --------------------------------------------------
# Randomize single columns to...
# --------------------------------------------------


#      Randomize the data following the same distribution for each column
#      Induce an error in each datacell of a 5% (default) in order to avoid indivual datapoints identifications