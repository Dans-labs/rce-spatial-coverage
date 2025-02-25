import json
import pandas as pd
import os
import re

def get_doi(json):
    full_id = json['@id']
    
    if '.org' in full_id: 
        doi = full_id.split('.org/')[-1]

    else:
        doi = full_id.split('doi:')[-1]

    return doi



def get_json_paths(prefix='geo'):
    # Extract info from JSONs 

    json_files = []

    for (root, dirs, file) in os.walk('../jsons'):
        for f in file:
            if f.endswith('.json') and f.startswith(f'{prefix}'):
                json_files.append(os.path.join(root, f))

    return json_files


def clean_description(description):
    """
    Clean the description values by removing the <p> and </p> tags.
    """
    if description:
        return re.sub(r'</?(p|b)>', '', description)
    return description



def extract_data(prefix = 'geo'): 
    # Create an empty list to store the data
    data = []

    json_files = get_json_paths(prefix)

    # Loop through each JSON file
    for file in json_files:
        with open(file, 'r') as f:
            json_data = json.load(f)
            
            # Extract the ID
            id = json_data.get('@id', None)
            if 'doi.org' in id: 
                id = id.split('doi.org/')[-1] # keep only the DOI part
            else: 
                id = id.split('doi:')[-1] 
            
            
            # Extract dataset descriptions, spatial coverage, and title
            describes = json_data.get('ore:describes', [])
            title = describes.get('title', None)

            if not isinstance(describes, list):
                describes = [describes]
            
            # Create empty lists to store the extracted data
            all_descriptions = []
            all_spatial_coverage_text = []
            all_spatial_points = []
            all_spatial_schemes = []

            for describe in describes:
                # Get dsDescriptionValue
                ds_description = describe.get('citation:dsDescription', [])
                if not isinstance(ds_description, list):
                    ds_description = [ds_description]
                
                for desc in ds_description:
                    descr = desc.get('citation:dsDescriptionValue', None)
                    if descr:
                        # Clean the description value
                        cleaned_descr = clean_description(descr)
                        all_descriptions.append(cleaned_descr)
                    
                # Get dansSpatialCoverageText
                spatial_coverage_text = describe.get('dansTemporalSpatial:dansSpatialCoverageText', [])
                if not isinstance(spatial_coverage_text, list):
                    spatial_coverage_text = [spatial_coverage_text]
                
                for text in spatial_coverage_text:
                    if text:
                        all_spatial_coverage_text.append(text)



                if prefix == 'geo': 
                     # Get dansSpatialPoint info
                    spatial_point = describe.get('dansTemporalSpatial:dansSpatialPoint', None)
                    if spatial_point:
                        if isinstance(spatial_point, list):
                            for point in spatial_point:
                                spatial_point_values = [
                                    point.get('dansTemporalSpatial:dansSpatialPointX', None),
                                    point.get('dansTemporalSpatial:dansSpatialPointY', None)
                                ]
                                spatial_scheme = point.get('dansTemporalSpatial:dansSpatialPointScheme', None)
                                all_spatial_points.append(spatial_point_values)
                                all_spatial_schemes.append(spatial_scheme)
                        else:
                            spatial_point_values = [
                                spatial_point.get('dansTemporalSpatial:dansSpatialPointX', None),
                                spatial_point.get('dansTemporalSpatial:dansSpatialPointY', None)
                            ]
                            spatial_scheme = spatial_point.get('dansTemporalSpatial:dansSpatialPointScheme', None)
                            all_spatial_points.append(spatial_point_values)
                            all_spatial_schemes.append(spatial_scheme)
                    else:
                        all_spatial_points.append([None, None])
                        all_spatial_schemes.append(None)


            



            # Append the extracted data to the list
            data.append({
                'id': id,
                'title': title,
                'dsDescriptionValues': all_descriptions[0],
                'dansSpatialCoverageText': all_spatial_coverage_text
            })

            if prefix == 'geo': 
                # Convert spatial points to a single string separated by ';'
                spatial_points_str = '; '.join([f"{x}, {y}" if x is not None and y is not None else "None,None" for x, y in all_spatial_points])

                data[-1]['dansSpatialPoints'] = spatial_points_str
                data[-1]['dansSpatialSchemes'] = all_spatial_schemes[0]
            

    return data

