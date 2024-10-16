def set_folder_path(self, folder_path:str):
    '''
    Set the folder path for the analysis

    Parameters
    ----------
    folder_path : str
        The folder path where the analysis will be saved
    '''
    self.folder_path = folder_path
    self.update()

def get_folder_path(self):
    '''
    Get the folder path for the analysis
    '''
    return self.folder_path

def set_filename(self, filename:str):
    '''
    Set the filename for the analysis

    Parameters
    ----------
    filename : str
        The filename for the analysis
    '''
    self.filename = filename
    self.update()
    return 0

def get_filename(self):
    '''
    Get the filename for the analysis
    '''
    return self.filename
