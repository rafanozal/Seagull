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
HTML_TEMPLATES_FOLDER = os.path.join(RES_FOLDER, "HTML")
HTML_NUMERICAL_CATEGORICAL_TEMPLATE = os.path.join(HTML_TEMPLATES_FOLDER, "Numerical_Categorical.html")




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