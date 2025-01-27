#!/usr/bin/env python3

'''

This file contain the getters and setters for the Seagull class.

This only contain functions affecting only the attributes of the class.
Other functions that might change the attributes must use this attributes only.

'''
    
    
# -----------------------------------------------------------------------------
# GETTERS
# -----------------------------------------------------------------------------

# Panda object
def get_data(self):
    return self.data
get_panda = get_data # alias

# Total columns
def ncol(self):
    return self.totalColumns
getTotalColumns = ncol # alias

# Total Rows
def nrow(self):
    return self.totalRows
getTotalRows = nrow # alias

# Name
def get_name(self):
    return self.name


# -----------------------------------------------------------------------------
# SETTERS
# -----------------------------------------------------------------------------

# Panda data
def setData(self, pandaObject):
    self.data = pandaObject
setPanda = setData # alias

# Total rows
def setTotalRows(self, totalR):
    self.totalRows = totalR

# Total columns
def setTotalColumns(self, totalC):
    self.totalColumns = totalC