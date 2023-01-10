import requests
from dotenv import load_dotenv
import os

load_dotenv()
directus_static_token = os.environ.get('DIRECTUS_STATIC_TOKEN')
directus_url = os.environ.get('DIRECTUS_URL')

def get_directus_info(endpoint):
    """Function for retrieving information from Directus, will work with any 'GET' API call

    Args:
        endpoint (string): API endpoint you wish to retrieve information from (see Directus API docs for full list)

    Returns:
        list: data returned from the request when request_status is 200 
        bool: a False flag for unsuccessful API calls 
    """
    header = {
        "Authorization" : f'access_token {directus_static_token}'
    }

    request_url = f'{directus_url}{endpoint}?access_token={directus_static_token}'

    r = requests.get(request_url, headers=header)

    if r.status_code == 200:
        r = r.json()
        data = r.get('data')
        return data
    else:
        print(r.text)
        return False

def get_collections(include_default_collections=False):
    """Retrieves collections using the Directus API, includes a control for filtering out collections automatically created by Directus

    Args:
        include_default_collections (bool, optional): Allows control over whether automatically generated collections are returned. Defaults to False.

    Returns:
        list: collections returned by the directus API
        bool: a False flag for unsuccessful API calls
    """
    collections = get_directus_info('collections')

    if not collections:
        print('Unable to retrieve collections from Directus. Check logs for more information')
        return False

    # Filter out default collections created by Directus i.e. those prepended with 'directus_"
    if not include_default_collections:
        collections = [collection for collection in collections if not collection['collection'].startswith("directus_")]
    
    return collections

