import os
import numpy as np
import pandas as pd

# Let's prepare the folder where to save the files
# Root folder with everything inside
cwd = os.getcwd()



# /datasets/ with different toy datasets
DATASET_FOLDER_PATH = os.path.join(cwd, "datasets")
SPOTIFY_PATH        = os.path.join(DATASET_FOLDER_PATH, 'spotify-2023.csv')
IRIS_PATH           = os.path.join(DATASET_FOLDER_PATH, 'iris_dataset.csv')

# /out/
OUT_FOLDER           = os.path.join(cwd, "out")
# /out/Examples/
EXAMPLES_PATH        = os.path.join(OUT_FOLDER, 'Examples')

# /out/Examples/Analysis/
EXAMPLES_ANALYSIS_PATH = os.path.join(EXAMPLES_PATH, 'Analysis')
# /out/Examples/Analysis/Numerical_Univariate/
EXAMPLES_ANALYSIS_NUMERICAL_UNIVARIATE_PATH = os.path.join(EXAMPLES_ANALYSIS_PATH, 'Numerical_Univariate')

# /out/Examples/Plots/
EXAMPLES_PLOTS_PATH  = os.path.join(EXAMPLES_PATH, 'Plots')
DENSITY_PLOTS_PATH   = os.path.join(EXAMPLES_PLOTS_PATH, 'Density_Plots')
HISTOGRAM_PLOTS_PATH = os.path.join(EXAMPLES_PLOTS_PATH, 'Histogram_Plots')


# /trash/ folder for the testing (ignored in the repository)
TRASH_FOLDER = os.path.join(cwd, "trash")

# /res/ folder with resources
RES_FOLDER            = os.path.join(cwd, "res")
CSS_TEMPLATES_FOLDER  = os.path.join(RES_FOLDER, "CSS")
CSS_SEAGULL_STYLE     = os.path.join(CSS_TEMPLATES_FOLDER, "Seagull_Style.css")

HTML_TEMPLATES_FOLDER = os.path.join(RES_FOLDER, "HTML")
HTML_NUMERICAL_CATEGORICAL_TEMPLATE = os.path.join(HTML_TEMPLATES_FOLDER, "Numerical_Categorical.html")
HTML_NUMERICAL_UNIVARIATE_TEMPLATE  = os.path.join(HTML_TEMPLATES_FOLDER, "Numerical_Univariate.html")

# Special characters
# Emojis for HTML
EMOJI_CHECK_CORRECT = "\u2705"
EMOJI_CHECK_FAIL    = "\u274C"  

# Special values
INTEGER_NAN     = np.nan
FLOAT_NAN       = np.nan
STRING_NAN      = np.nan
CATEGORICAL_NAN = pd.NA
DATA_NAN        = pd.NaT

INTEGER_ZERO     = 0
FLOAT_ZERO       = 0.0
STRING_ZERO      = '0'
CATEGORICAL_ZERO = "Uknown"
DATA_ZERO        = pd.NaT


# Valid types
BOOL_TYPES        = ["bool", "boolean", "Boolean", bool]

#INTEGER_TYPES     = ["int32", "int64", "Int32", "Int64",
#                     int, pd.Int8Dtype, pd.Int16Dtype, pd.Int32Dtype, pd.Int64Dtype,
#                     np.int32, np.int64, int]

#FLOAT_TYPES       = ["float32", "float64", "Float32", "Float64",
#                     float, pd.Float32Dtype, pd.Float64Dtype,
#                     np.float32, np.float64, float]

INTEGER_TYPES     = [int, pd.Int8Dtype, pd.Int16Dtype, pd.Int32Dtype, pd.Int64Dtype,
                     np.int32, np.int64, np.dtypes.Int64DType, np.dtypes.Int32DType, np.dtypes.Int16DType, np.dtypes.Int8DType]

FLOAT_TYPES       = [float, pd.Float32Dtype, pd.Float64Dtype,
                     np.float32, np.float64, np.dtypes.Float64DType, np.dtypes.Float32DType]
 


STRING_TYPES      = ["str", "string", "String", "object",
                     str, pd.StringDtype]

CATEGORICAL_TYPES = ["categorical", "Categorical", "object", "category",
                     pd.CategoricalDtype]

DATE_TYPES        = ["datetime64", "datetime64[ns]", "datetime64[ns, UTC]",
                     pd.DatetimeTZDtype, pd.Timestamp]

NUMERICAL_TYPES   = INTEGER_TYPES + FLOAT_TYPES
SOFT_CATEGORIES   = STRING_TYPES  + CATEGORICAL_TYPES
ALL_TYPES         = STRING_TYPES  + CATEGORICAL_TYPES + BOOL_TYPES + INTEGER_TYPES + FLOAT_TYPES + DATE_TYPES


INVALID_CATEGORIES = [pd.NA, np.nan, None]