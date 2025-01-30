import requests
import json
import time
# import pprint

def get_json(doi): 
    """
    Get JSON data of a dataset from the Archaeology Data Stations API.
    Wait for 1 second between requests to avoid overloading the server.

    :param doi: DOI of the dataset 
    :return: JSON data of the dataset 
    """

    url = f"https://archaeology.datastations.nl/api/datasets/export?exporter=OAI_ORE&persistentId={doi}"

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        print(url)

        # Check if the request was successful
        response.raise_for_status()

        # Parse the JSON data
        data = response.json()

        # Optionally, save it to a file
        out_path = f'../jsons/geo_{doi.replace('/', '%')}.json'


        with open(out_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"JSON data has been saved to '{out_path}'.")
        # pprint.pprint(data) 

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    # Wait for 1 second to avoid overloading the server
    wait_time = 1  # seconds
    time.sleep(wait_time)

