import requests
import zipfile
import io
import os

def download_files(persistent_id, selected_files):

    url = f"http://archaeology.datastations.nl/api/access/dataset/:persistentId?persistentId=doi:{persistent_id}"
    params = {"persistent_id": persistent_id}

    output_doi = persistent_id.replace("/", "%")
    output_dir = f"../data/downloaded_files/{output_doi}"


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


def download_pdf(persistent_id): 

    url = f"http://archaeology.datastations.nl/api/access/dataset/:persistentId?persistentId=doi:{persistent_id}"
    params = {"persistent_id": persistent_id}

    output_doi = persistent_id.replace("/", "%")
    output_dir = f"../data/reports/{output_doi}"

    response = requests.get(url, params=params, stream=True)

    if response.status_code == 200:

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            os.makedirs(output_dir, exist_ok=True)

            zip_filenames = set(zip_file.namelist())  # Get all files in the ZIP
            print(zip_filenames)
            pdf_files = {file_name for file_name in zip_filenames if file_name.endswith('.pdf')}

            for file_name in pdf_files:
                zip_file.extract(file_name, output_dir)
                print(f"Extracted: {file_name}")

        print(f"PDF files saved to '{output_dir}'")
    else:
        print(f"Error: {response.status_code}, {response.text}")

    print("=================================================================")