'''
Author : Animesh Bhasin
Version : 1
Version Date : 16th Nov 2022
Description : This script is to preprocess the crashes data
'''

import requests
import get_crashes
import pandas as pd
from datetime import date, timedelta, datetime
from sqlalchemy import create_engine
import json
import googlemaps
from utils.gmaps_api import get_zipcode, get_lat_long
import os

def main():
    '''main function'''
    print ("Script started at " + str(datetime.now()))
    database_url = os.getenv('database_url')
    schema_name = 'crash'
    crashes_table_name = 'crashes_clean'
    # Connect to database
    engine = create_engine(database_url, echo=False)
    # Find maximum date for which data is present in db( to intelligently incrementally process data)
    crash_start_date = get_crashes.get_date_max_date_in_db(engine, schema_name, crashes_table_name)
    # Find dates to process
    date_list = get_crashes.get_list_of_dates_to_process(crash_start_date)
    start_date = date_list[0]
    end_date = date_list[-1]

    #SQL query to read data
    sql_statement = '''select * from crash.crashes where date(crash_date) between '{}' and '{}';'''.format(start_date,
                                                                                                          end_date)
    #Read the SQL query data into a dataframe
    df = pd.read_sql_query(sql_statement, database_url)

    #Create google Maps Client for filling missing pincodes/lat/long
    gmaps = googlemaps.Client(key=os.getenv('gmaps_key'))
    if not df.empty:
        '''Fill missing zipcode'''
        mask = (df['zip_code'].isna()) & (df['location_latitude'] != 0) & (df['location_latitude'].notna())

        if mask.any():
            df.loc[mask, 'zip_code'] = df.loc[mask].apply \
                (get_zipcode, axis=1, gmaps = gmaps, lat_field='location_latitude', lon_field='location_longitude')

        '''Fill missing lat long'''
        mask = ((df['location_latitude'].isna()) | (df['location_latitude'] == '0')) & (df['zip_code'].notna())
        if mask.any():
            df.loc[mask, ['location_latitude', 'location_longitude']] = df.loc[mask].apply(get_lat_long, axis=1, gmaps = gmaps).tolist()

        '''Write data to clean table'''
        write_to_db(engine, df, collision_id_list_str=get_collision_id_list(df), schema_name='crash',
                    table_name='crashes_clean')
    print ("Script ended at " + str(datetime.now()))


def get_collision_id_list(df):
    """
    Function to convert json data to dataframe

    Args:
        df(Dataframe) : Dataframe containing collisions data
    Returns:
        collision_id_list_str(str) : A String of list of collision ids being processed needed so that
                        existing collision id records can be deleted from database before inserting them
                        to avoid duplicates in database
    """
    collision_id_list = df['collision_id'].tolist()

    collision_id_list_str = str(collision_id_list)[1:-1]

    return collision_id_list_str


def write_to_db(engine, df, collision_id_list_str, schema_name, table_name):
    """
    Function to write the dataframe to database

    Args:
        engine (SQLAlchemyEngine): SQL Alchemy engine created from database
        df(Dataframe) : Dataframe containing collisions data
        collision_id_list_str(str) : A String of list of collision ids being processed needed so that
                existing collision id records can be deleted from database before inserting them
                to avoid duplicates in database
        schema_name(str): Schema Name
        table_name(str): Table Name

    """
    sql_statement = 'delete from {}.{} where collision_id in ({})'.format(schema_name, table_name,
                                                                          collision_id_list_str)

    engine.execute(sql_statement)
    df.to_sql(name=table_name, schema=schema_name, con=engine, if_exists='append', index=False)


if __name__ == '__main__':
    main()
