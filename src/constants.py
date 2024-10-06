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

# /out/ folder for the examples
OUT_FOLDER   = os.path.join(cwd, "out")
# /trash/ folder for the testing (ignored in the repository)
TRASH_FOLDER = os.path.join(cwd, "trash")

# /res/ folder with resources
RES_FOLDER            = os.path.join(cwd, "res")
CSS_TEMPLATES_FOLDER  = os.path.join(RES_FOLDER, "CSS")
CSS_SEAGULL_STYLE     = os.path.join(CSS_TEMPLATES_FOLDER, "Seagull_Style.css")

HTML_TEMPLATES_FOLDER = os.path.join(RES_FOLDER, "HTML")
HTML_NUMERICAL_CATEGORICAL_TEMPLATE = os.path.join(HTML_TEMPLATES_FOLDER, "Numerical_Categorical.html")

# Special characters
# Emojis for HTML
EMOJI_CHECK_CORRECT = "\u2705"
EMOJI_CHECK_FAIL    = "\u274C"  

# Special values
INTEGER_NAN     = np.nan
FLOAT_NAN       = np.nan
STRING_NAN      = np.nan
CATEGORICAL_NAN = np.nan
DATA_NAN        = pd.NaT

INTEGER_ZERO     = 0
FLOAT_ZERO       = 0.0
STRING_ZERO      = '0'
CATEGORICAL_ZERO = "Uknown"
DATA_ZERO        = pd.NaT