import os

# Let's prepare the folder where to save the files
# Root folder with everything inside
cwd = os.getcwd()
# /datasets/ with different toy datasets
DATASET_FOLDER_PATH = os.path.join(cwd, "datasets")
SPOTIFY_PATH        = os.path.join(DATASET_FOLDER_PATH, 'spotify-2023.csv')
IRIS_PATH           = os.path.join(DATASET_FOLDER_PATH, 'iris_dataset.csv')

# /out/ folder for tests
OUT_FOLDER = os.path.join(cwd, "out")

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


# Testing...
def main():

    print("Current folder:")
    print(cwd)
    print()
    print("/out/ folder:")
    print(OUT_FOLDER)
    print()

if __name__ == "__main__":
    main()