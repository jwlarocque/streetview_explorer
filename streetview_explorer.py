# Author: John LaRocque
# Convenience wrapper for Google's Static Streetview API
# Loosely based on https://github.com/robolyst/streetview
# WIP, extremely naive

import requests
import pdb

# GCP key
key = "AIzaSyBMvJJ-rezXdRPiiOdvp79G1sBCvMJPpw0"

# == Metadata =======================================================

# metadata_cache is a dictionary of dictionaries
# Primary keys are (lat, lon) tuples with 3 decimal places of precision (approx. 100 meter squares referred to as "regions")
# Secondary keys are (lat, lon) tuples with full precision (as returned by the API)
# Secondary items are {"date": "", "pano_id": ""}
metadata_cache = {}

def get_region(lat, lon):
    return (round(lat, 3), round(lon, 3))

# TODO: is radius a valid param (undocumented) (also source (default/outdoor))
def _get_loc_metadata(lat, lon):
    metadata_url = "https://maps.googleapis.com/maps/api/streetview/metadata?location={},{}&key={}"
    return requests.get(metadata_url.format(lat, lon, key))

def cache_response(response):
    coords = (response["location"]["lat"], response["location"]["lng"])
    if coords not in metadata_cache:
        print(coords) # TODO: remove debug
        metadata_cache[coords] = {"date": response["date"], "pano_id": response["pano_id"]}

# Fetches streetview metadata for a given location
# Note: requests to this API are free!
def fetch_metadata(lat, lon):
    response = _get_loc_metadata(lat, lon)
    if response == None:
        print("Request failed, response was None.")
        return None # TODO: return something other than none?
    if response.status_code != 200:
        # TODO: repeat request on some stauses?
        print("Unexpected response status: {}".format(response.status_code))
        return None # TODO: return something other than none?
    result = eval(response.content)
    cache_response(result)
    return result

# Searches for panoramas in a 1/1,000 region
# with 1/10,000 separation
# returns nothing (fetch_metadata caches the results)
# TODO: make this more intelligent
#       for example, search adjacent to known pano coords
def get_region_metadata(lat, lon):
    region = (round(lat, 3), round(lon, 3))
    for i in range(0, 10):
        for j in range(0, 10):
            fetch_metadata(lat + 0.0001 * i, lon + 0.0001 * j)

# == Panoramas ======================================================

def _get_pano_tile(pano_id, heading, pitch, fov, width, height):
    pano_url = "https://maps.googleapis.com/maps/api/streetview?pano={}&size={}x{}&heading={}&pitch={}&key={}"
    return requests.get(pano_url.format(pano_id, width, height, heading, pitch, key))

def fetch_pano_tile(pano_id, heading, pitch, fov=90, width=640, height=640):
    response = _get_pano_tile(pano_id, heading, pitch, fov, width, height)
    if response == None:
        print("Request failed, response was None.")
    if response.status_code != 200:
        # TODO: repeat request on some stauses?
        print("Unexpected response status: {}".format(response.status_code))
    return response
