# General libraries
import numpy as np

# Set the data x
def set_data_x(self, data_x):
    '''
    Set the data x

    Parameters
    ----------
    data_x : array_like
        The data x
    '''
    self.data_x = np.sort(data_x)
