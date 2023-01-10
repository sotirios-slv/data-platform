import os

import requests
from dotenv import load_dotenv

load_dotenv()
directus_static_token = os.environ.get("DIRECTUS_STATIC_TOKEN")
directus_url = os.environ.get("DIRECTUS_URL")
staging_table = os.environ.get("STAGING_TABLE")


def get_directus_info(endpoint):
    """Function for retrieving information from Directus, will work with any 'GET' API call

    Args:
        endpoint (string): API endpoint you wish to retrieve information from (see Directus API docs for full list)

    Returns:
        list: data returned from the request when request_status is 200
        bool: a False flag for unsuccessful API calls
    """

    request_url = f"{directus_url}{endpoint}?access_token={directus_static_token}"

    r = requests.get(request_url)

    if r.status_code == 200:
        r = r.json()
        data = r.get("data")
        return data
    else:
        print(r.text)
        return False
