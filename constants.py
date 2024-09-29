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


#DATASET_FOLDER_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets')
#SPOTIFY_PATH        = os.path.join(DATASET_FOLDER_PATH, 'spotify-2023.csv')

# Go up three levels
#pre1_dir = os.path.abspath(os.path.join(cwd,      os.pardir))
#pre2_dir = os.path.abspath(os.path.join(pre1_dir, os.pardir))
#pre3_dir = os.path.abspath(os.path.join(pre2_dir, os.pardir))

# Go into the "folder_A" directory
#TEST_FOLDER = os.path.join(pre3_dir, "segull_test")

#print(TEST_FOLDER)

def main():

    print("Current folder:")
    print(cwd)
    print()
    print("/out/ folder:")
    print(OUT_FOLDER)
    print()

if __name__ == "__main__":
    main()