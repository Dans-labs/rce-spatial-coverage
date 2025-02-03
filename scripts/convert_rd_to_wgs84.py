
import requests
import pyproj


def clean_api_output(response_text):
    """
    Clean the output of the API call and turn it into a dictionary
    Currently only works for one coordinate pair
    """

    split = response_text.strip().split('\n')

    coords = []
    for coord in split:
        s = coord.split('\t')
        s_clean = [item.replace(':', '') for item in s]
        s_clean = [item.replace('(X,Y)', '') for item in s_clean]
        s_clean = [item.replace('(E,N)', '') for item in s_clean]
        coords.append(s_clean)

    coord_dict = {k: v for k, v in coords}
    return coord_dict



def query_api(coord1, coord2):

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        'Referer': 'https://www.regiolab-delft.nl/public/rd_wgs84.html',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',
    }

    params = {
        'coordinate1': f'{coord1}',
        'coordinate2': f'{coord2}',
        'format': 'text',
        'retrieve': 'Submit query',
    }

    response = requests.get('https://www.regiolab-delft.nl/road_mapping/rd_wgs84.cgi', params=params, headers=headers)
    response_text = response.text

    clean_text = clean_api_output(response_text)

    return clean_text



def convert_rd_to_wgs84(rd_coordinates):
    """
    Convert RD (Rijksdriehoek) coordinates to WGS84 coordinates.
    """
    rd_proj = pyproj.Proj(init='epsg:28992')
    wgs84_proj = pyproj.Proj(init='epsg:4326')

    if isinstance(rd_coordinates, list):
        wgs84_coordinates = []
        for rd_coord in rd_coordinates:
            x, y = rd_coord
            lon, lat = pyproj.transform(rd_proj, wgs84_proj, x, y)
            wgs84_coordinates.append((lat, lon))
        return wgs84_coordinates
    else:
        x, y = rd_coordinates
        lon, lat = pyproj.transform(rd_proj, wgs84_proj, x, y)
        return (lat, lon)
    

# Function to convert and handle multiple coordinate pairs
def convert_multiple_pairs(row):
    rd_points_str = row['dansSpatialPoints']
    scheme = row['dansSpatialSchemes']
    
    if scheme == 'longitude/latitude (degrees)':
        return rd_points_str
    elif rd_points_str == 'None,None':
        return 'None'
    else:
        rd_points = [tuple(map(float, point.split(','))) for point in rd_points_str.split(';')]
        wgs84_points = convert_rd_to_wgs84(rd_points)
        return ';'.join([f"{lat},{lon}" for lat, lon in wgs84_points])