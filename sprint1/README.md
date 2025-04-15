# Notes on RCE Kaart - Sprint 1


## Task 1: identify & infer datasets with coordinates but missing coordinates scheme or incomplete coordinates
You can find the code used to identify datasets with missing coordinate schemes in [sprint_1.ipynb]("sprint_1.ipynb"). I collected the number of datasets that have values for SpatialPointX and SpatialPointY, but no SpatialPointSchema, as well as datasets that use Bounding Boxes to express coordinates, but no scheme specification. 

I also counted and collected the datasets that have incomplete coordinates (e.g. values for BoundingBoxEast and West, but not North and South). See the counts in the table below. All datasets that have *incomplete coordinates* use bounding boxes. X/Y points seem to be complete. 



| # SpatialPoint | # Bounding Box| incomplete coordinates |
| ----------------- | --------------- | ---------------------- |
| 270               | 3               | 8                      |

*Table 1: The number of datasets with a missing value for the coordinate scheme or incomplete coordinates*


### Steps 
1: **Update** the MongoDB instance to include the most recent deposits. It only contains published datasets, no drafts etc. 

2: **Identify** the datasets that have coordinate values, but no value for the scheme with a query. Collect them in a JSON file containing the dataset url, coordinate points, and author. 

3:  **Infer** the scheme that corresponds to the coordinates with help of the rules.

4: **Write** the inferred scheme out to the JSON, along with a boolean variable to indicate a change happened. 


### Notes on the inference of schemes
- 156 of 273 missing schemes are by the same author. Conveniently, the schemes  are the same for all datasets deposited by this author. 
- The remaining instances of missing schemes are inferred based on the rules below (expressed as regular expressions). I wrote the rules by inspecting the coordinates, placing some of them on a map, and consulting with Hella. 
	- if author = "Boter, Reinoud": scheme = long/lat 
	- if format is like "122.110, 481.405": assume the point should be gone and it's RD. 
		- if format is like "195149.05, 324030.26" or "121960.00, 488620.00": assume RD 
	- Points like "132230, 502955": assume RD
	- Points like "98800, 440006": assume RD 
	- Points like "6.56702, 53.21868": assume long/lat (wrong order, should be switched around later) 
	- Points like "52.131144, 4.655521": assume long/lat (in the correct order)
- The code was written for the inferring of Points, not Bounding Boxes (although it would work with minor additions). Since there are so few instances of schemes missing for bounding boxes (only 3), it was faster to infer them manually. The same rules were used as for the automatic inference of point schemes. 
- I added a boolean variable called `incorrect` that indicates if a long/lat variable is probably reversed (y,x instead of x,y). 
- The code only works when there is exactly one entry for the points. In one case, there is more than one. Add these manually. 
  



## Task 2: Update metadata 
The [Dataverse documentation](https://guides.dataverse.org/en/latest/api/native-api.html#update-metadata-for-a-dataset) specifies how you can add metadata for fields that are empty or accept multiple values. You can also replace existing metadata by changing a parameter (useful for incorrect coordinates). When adding or replacing the values of certain fields, you only need to edit those fields in a JSON.  

The following code block is copied from the [Dataverse documentation](https://guides.dataverse.org/en/latest/api/native-api.html#update-metadata-for-a-dataset), and shows how to populate metadata fields. 

```
export API_TOKEN=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
export SERVER_URL=https://demo.dataverse.org
export PERSISTENT_IDENTIFIER=doi:10.5072/FK2/BCCP9Z

curl -H "X-Dataverse-key: $API_TOKEN" -X PUT "$SERVER_URL/api/datasets/:persistentId/editMetadata?persistentId=$PERSISTENT_IDENTIFIER&replace=true" --upload-file dataset-update-metadata.json
```

Fields needed in the JSON: 
- dataset PIDs
- SpatialPointScheme inferred value 
