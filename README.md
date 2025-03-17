# Enrichment of Geospatial Metadata in the DANS Archaeology Data Station 
This repository contains the code that was used to research and implement the enrichment of geospatial metadata in the [Archaeology Data Station](https://archaeology.datastations.nl/). The goal is to identify where geospatial metadata in the form of coordinates or toponyms is missing, and how it can be extracted from other parts of the metadata or files. 



## Structure 
Most exploratory work was done in Python notebooks. Functions from the `scripts` folder are used throughout the notebooks. 

### Folder description
- `collect_data` for Notebooks that extract dataset metadata or data files from the Data Station. 
- `explore_data` for Notebooks that explore the structure of the extracted data, or the distribution and values of certain metadata fields. 
- `coordinates` for (draft) solutions relating to enrichment or alignment of coordinates in the metadata. 
- `scripts` for scripts with functions that are used in the notebooks. 

### File Description
- `collect_data/data_preparation.ipynb`: extract DOIs from an existing export of the Data Station's metadata 
- `collect_data/collect_metadata.ipynb`: extract complete metadata records based on DOI, store in local MongoDB instance. 
- `collect_data/extract_files.ipynb`: so far, it can display all files in a dataset, download all files, download only specified files, and download all files of a specified type. it takes dataset DOIs as input. 
- `explore_data/explore_jsons`: looks into the JSONs that are extracted in `collect_metadata`. It displays basic stats (dataset size, counts of certain metadata fields), and identifies datasets with missing geospatial data. It allows you to select datasets on certain conditions (e.g. all PAN datasets, all datasets that have a value the dansSpatialPoint field), explore them, and write them out to your disk. 
- `coordinates/placename_to_coordinates.ipynb:`: exploration of how well toponyms can be mapped to coordinates with Open Street Map. Seems to work for most Dutch placename, if data is cleaned. 
- `coordinates/rd_to_WGS84.ipynb`: applies the function to map Rijksdriehoek to WGS84 coordinates (or the other way around). Takes the ouput of `placename_tocoordinates` as input.
- `coordinates/polygons.ipynb`: extracts polygons from PAN xmls that are downloaded with `extract_files`, converts them to bounding boxes (this last step is unverified). 
- `coordinates/map_display.ipynb`: allows for the visualisation of coordinates/polygons on a map in browser.
- `scripts/convert_rc_to_wgs84.py`: contains multiple approaches to map Rijksdriehoek to WGS84 (via an API, using a Python package). Also includes a function that can deal with rows that have multiple coordinate pairs as entry. 
- `scripts/doi_to_json.py`: contains a function that extracts a JSON with metadata from a DOI and saves it to disk. (only used in early stages)
- `scripts/download_ds_files.py`: contains the functions with the functionality described for `explore_jsons`. 
- `scripts/json_to_df.py`: contains functions that extract and clean data from the metadata JSON, format them as a DataFrame, and extracts DOIs from a JSON. 


