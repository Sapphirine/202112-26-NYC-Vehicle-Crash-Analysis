"""
Author : Abhishek Arora
Version : 1
Version Date : 29th Nov 2021
Description : Util script to get pincode/lat/long using Google Maps API
"""


import json
import googlemaps
from datetime import datetime
import os

gmaps = googlemaps.Client(key=os.getenv('gmaps_key'))


def get_zipcode(df, gmaps, lat_field, lon_field):
    """
    Function to get zipcode field for a dataframe from lat long field

    Args:
        df (dataframe): input dataframe
        gmaps (googlemaps.Client): [Google Maps Authenticated client]
        lat_field (string) : [name of latitude field in dataframe]
        lon_field (string) : [name of longitude field in dataframe]
    Returns:
        get_zipcode (string): Retrieved pincode from lat long
    """
    reverse_geocode_result = gmaps.reverse_geocode((df[lat_field], df[lon_field]))
    s1 = json.dumps(reverse_geocode_result)
    address_response = json.loads(s1)
    if address_response:
        get_zipcode = address_response[0]['address_components'][-1]['long_name']
        return get_zipcode
    return None


def get_lat_long(row, gmaps):
    """
    Function to get lat long value for a dataframe row containing zipcode

    Args:
        row (dictionary): each row of Dataframe
        gmaps (googlemaps.Client): [Google Maps Authenticated client]

    Returns:
        get_lat (float): Retrieved latitide
        get_long (float) :  Retrieved longitude
    """
    zipcode = row['zip_code']
    geocode_result = gmaps.geocode(zipcode)

    get_lat, get_long = 0.0, 0.0
    if geocode_result:
        for i in geocode_result[0]['geometry']['bounds']:
            get_lat = geocode_result[0]['geometry']['bounds'][i]['lat']
            get_long = geocode_result[0]['geometry']['bounds'][i]['lng']
            break
    return get_lat, get_long