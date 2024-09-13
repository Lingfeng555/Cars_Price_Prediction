import pandas as pd
import os

def delete_photos(file_list, file_directory):
    for filename in file_list:
        file_path = os.path.join(file_directory, filename + ".jpg")
        try:
            os.remove(file_path)
            print(f"Deleted {filename}")
        except FileNotFoundError:
            print(f"{filename} not found.")
        except PermissionError:
            print(f"No permission to delete {filename}.")
        except Exception as e:
            print(f"Error deleting {filename}: {str(e)}")

def main():
    #Load both .csv
    groundTruth = pd.read_csv("data/GroundTruth.csv")
    metaData = pd.read_csv("data/metadata.csv")

    print(metaData.info())

    #Remove unneccesary columns
    columns = ["attribution", "copyright_license", "acquisition_day", "benign_malignant", "clin_size_long_diam_mm", "concomitant_biopsy", 
           "diagnosis","diagnosis_confirm_type","family_hx_mm","fitzpatrick_skin_type","image_type","lesion_id","mel_class",
           "mel_mitotic_index","mel_thick_mm","mel_type","mel_ulcer","melanocytic","nevus_type","patient_id","personal_hx_mm",
           "pixels_x","pixels_y", "dermoscopic_type"]
    metaData.drop(columns, axis=1, inplace = True)

    #Merge both dataframe
    result = pd.merge(metaData, groundTruth, left_on='isic_id', right_on='image', how='inner')

    #Clean unneccesary data
    result.drop("image", axis=1, inplace = True)

    rows_with_nan = result[result.isna().any(axis=1)]
    pictures_to_be_removed = rows_with_nan["isic_id"].to_list()
    delete_photos(pictures_to_be_removed, "data/images/")

    result.dropna(inplace = True)
    #Write the result
    print(result.info())
    result.to_csv('skinData.csv', index=False)

if __name__ == '__main__' : main()