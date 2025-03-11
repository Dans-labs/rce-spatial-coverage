# This script contains functions to inspect and download files from a dataset in the Archaeology Data Station repository.
# Author: Alessandra Polimeno (DANS-KNAW)


# The format of the DOIs should have the following structure: "10.17026/dans-xxx-xx0x"
# They can be found under the column "dsPersistentID"

import requests
import zipfile
import io
import os


def print_all_files(persistent_id):
    """
    Print all files in a dataset with the given persistent ID.

    :param persistent_id: The persistent ID of the dataset.

    """
    url = f"http://archaeology.datastations.nl/api/access/dataset/:persistentId?persistentId=doi:{persistent_id}"
    params = {"persistent_id": persistent_id}

    response = requests.get(url, params=params, stream=True)

    if response.status_code == 200:

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            print(zip_file.namelist())
    else:
        print(f"Error: {response.status_code}, {response.text}")

    print("=================================================================")




def download_all_files(persistent_id, output_path):
    """
    Download all files from a dataset with the given persistent ID.

    :param persistent_id: The persistent ID of the dataset.
    :param output_path: The path to the directory where the files will be saved. If the directory does not exist, it will be created.

    """
    url = f"http://archaeology.datastations.nl/api/access/dataset/:persistentId?persistentId=doi:{persistent_id}"
    params = {"persistent_id": persistent_id}

    output_doi = persistent_id.replace("/", "%")
    output_dir = f"{output_path}/{output_doi}"

    response = requests.get(url, params=params, stream=True)

    if response.status_code == 200:

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            os.makedirs(output_dir, exist_ok=True)

            for file_name in zip_file.namelist():
                zip_file.extract(file_name, output_dir)
                print(f"Extracted: {file_name}")

        print(f"All files saved to '{output_dir}'")
    else:
        print(f"Error: {response.status_code}, {response.text}")   
    
    print("=================================================================")





def download_selected_files(persistent_id, selected_files, output_path):
    """
    Download selected files from a dataset with the given persistent ID. You select the files by providing a list of filenames.
    Even if you want to download only one file, you need to provide the filename as a list.

    :param persistent_id: The persistent ID of the dataset.
    :param selected_files: A list containing the filenames to be downloaded.
    :param output_path: The path to the directory where the files will be saved. If the directory does not exist, it will be created.

    """

    url = f"http://archaeology.datastations.nl/api/access/dataset/:persistentId?persistentId=doi:{persistent_id}"
    params = {"persistent_id": persistent_id}

    output_doi = persistent_id.replace("/", "%")
    output_dir = f"{output_path}/{output_doi}"

    response = requests.get(url, params=params, stream=True)

    if response.status_code == 200:

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            os.makedirs(output_dir, exist_ok=True)

            zip_filenames = set(zip_file.namelist())  # Get all files in the ZIP
            print(zip_filenames)
            found_files = selected_files.intersection(zip_filenames)
            # missing_files = selected_files - zip_filenames  # Files that are missing

            for file_name in found_files:
                zip_file.extract(file_name, output_dir)
                print(f"Extracted: {file_name}")

            #if missing_files:
            #    print(f"Warning: The following files were not found in the ZIP: {missing_files}")

        print(f"Selected files saved to '{output_dir}'")
    else:
        print(f"Error: {response.status_code}, {response.text}")

    print("=================================================================")





def download_specific_filetype(persistent_id, output_path, filetype): 
    """
    Download all files of a given filetype from the dataset with the specified persistent ID.

    :param persistent_id: The persistent ID of the dataset.
    :param output_path: The path to the directory where the PDF files will be saved. If the directory does not exist, it will be created.
    :param filetype: The file type to be downloaded as a string, e.g. 'xml'

    """

    url = f"http://archaeology.datastations.nl/api/access/dataset/:persistentId?persistentId=doi:{persistent_id}"
    params = {"persistent_id": persistent_id}

    output_doi = persistent_id.replace("/", "%")
    output_dir = f"{output_path}/{output_doi}"

    response = requests.get(url, params=params, stream=True)

    if response.status_code == 200:

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            os.makedirs(output_dir, exist_ok=True)

            zip_filenames = set(zip_file.namelist())  # Get all files in the ZIP
            print(zip_filenames)
            selected_files = {file_name for file_name in zip_filenames if file_name.endswith(f'{filetype}')}

            for file_name in selected_files:
                zip_file.extract(file_name, output_dir)
                print(f"Extracted: {file_name}")

        print(f"{filetype} files saved to '{output_dir}'")
    else:
        print(f"Error: {response.status_code}, {response.text}")

    print("=================================================================")