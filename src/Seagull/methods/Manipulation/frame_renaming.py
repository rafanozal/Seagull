#!/usr/bin/env python3

'''

This file contain functions that rename the columns and rows of the dataframe

'''

# ---------------------------------
# RENAMING
# ---------------------------------
# region

# Rename all columns
def rename_columns(self, newNames):
    self.data = self.data.set_axis(newNames, axis=1, copy=False)

setColumnsNames = rename_columns
renameColumns   = rename_columns

# Rename ONE column
def rename_column(self, columnIndex, newName):
    self.data.rename(columns={self.data.columns[columnIndex]: newName}, inplace=True)

setColumnName   = rename_column
renameColumn    = rename_column

# Rename all rows
def rename_rows(self, newNames):
    self.data = self.data.set_axis(newNames, axis=0, copy=False)

setRowsNames    = rename_rows


# Rename ONE row
def rename_row(self, rowIndex, newName):
    self.data.rename(rows={self.data.rows[rowIndex]: newName}, inplace=True)

set_row_name    = rename_row

# Rename the entire frame
def rename_frame(self, new_name):
    self.data.name = new_name
set_name        = rename_frame

# endregion
