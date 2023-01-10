import os

import requests
from directus_helpers import get_directus_info
from dotenv import load_dotenv

load_dotenv()
directus_static_token = os.environ.get("DIRECTUS_STATIC_TOKEN")
directus_url = os.environ.get("DIRECTUS_URL")
staging_table = os.environ.get("STAGING_TABLE")


def get_collections(include_default_collections=False):
    """Retrieves collections using the Directus API, includes a control for filtering out collections automatically created by Directus

    Args:
        include_default_collections (bool, optional): Allows control over whether automatically generated collections are returned. Defaults to False.

    Returns:
        list: collections returned by the Directus API
        bool: a False flag for unsuccessful API calls
    """
    collections = get_directus_info("collections")

    if not collections:
        print(
            "Unable to retrieve collections from Directus. Check logs for more information"
        )
        return False

    # Filter out default collections created by Directus i.e. those prepended with 'directus_"
    if not include_default_collections:
        collections = [
            collection
            for collection in collections
            if not collection["collection"].startswith("directus_")
        ]

    return collections


def create_collection(collection_name, metadata_fields):

    payload = {"collection": collection_name, "meta": metadata_fields}

    r = requests.post(
        f"{directus_url}collections?access_token={directus_static_token}", json=payload
    )

    if r.status_code != 200:
        print(r.status_code)
        print(r.json())
        return False

    return True


def create_staging_collection(collection_name):

    staging_table_metadata = get_directus_info(f"collections/{staging_table}")

    collection_name_updated = f"{collection_name}_stg"

    metadata_fields = {
        "collection": collection_name_updated,
        "group": staging_table,
        "icon": staging_table_metadata["meta"]["icon"],
        "color": staging_table_metadata["meta"]["color"],
        "note": f"Staging table for the {collection_name} collection. Contains data with minimal updates from the source",
    }

    staging_request = create_collection(collection_name_updated, metadata_fields)

    print(f"Staging collection request success: {staging_request}")

    return staging_request
