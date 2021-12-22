"""
Author : Animesh Bhasin
Version : 1
Version Date : 16th Nov 2022
Description : This script is to read the data from City of New York API and load into postgres db
"""

import requests
import pandas as pd
from datetime import date, timedelta
from sqlalchemy import create_engine
import os

def main():
    """
    Main function
    """
    crashes_url = 'https://data.cityofnewyork.us/resource/h9gi-nx95.json'
    column_list = ['crash_date', 'crash_time', 'borough', 'zip_code', 'location_latitude', 'location_longitude',
                   'location_location', 'on_street_name', 'off_street_name', 'cross_street_name',
                   'number_of_persons_injured', 'number_of_persons_killed', 'number_of_pedestrians_injured',
                   'number_of_pedestrians_killed', 'number_of_cyclist_injured', 'number_of_cyclist_killed',
                   'number_of_motorist_injured', 'number_of_motorist_killed', 'contributing_factor_vehicle_1',
                   'contributing_factor_vehicle_2', 'contributing_factor_vehicle_3', 'contributing_factor_vehicle_4',
                   'contributing_factor_vehicle_5', 'collision_id', 'vehicle_type_code1', 'vehicle_type_code2',
                   'vehicle_type_code_3', 'vehicle_type_code_4', 'vehicle_type_code_5']

    #Connect to database
    database_url = os.getenv('database_url')
    schema_name = 'crash'
    crashes_table_name = 'crashes'
    engine = create_engine(database_url, echo=False)

    #Find maximum date for which data is present in db( to intelligently incrementally process data)
    crash_start_date = get_date_max_date_in_db(engine, schema_name, crashes_table_name)

    #Find dates to process
    date_list = get_list_of_dates_to_process(crash_start_date)
    print ('Processing dates : {}'.format(date_list))

    #Process data for each date
    for crash_date in date_list:
        print('Processing date : {}'.format(crash_date))
        #Read data from API
        data = read_data_for_crash_date(crash_date, crashes_url)
        if data:
            #convert dictionary data to dataframe
            df, collision_id_list_str = get_data_df(data, column_list)
            #Write data to database
            write_to_db(engine, df, collision_id_list_str, schema_name, crashes_table_name)


def get_date_max_date_in_db(engine, schema_name, table_name):
    """
    Function to get max crash date from database

    Args:
        engine (SQLAlchemyEngine): SQL Alchemy engine created from database
        schema_name(str): Schema Name
        table_name(str): Table Name
    Returns:
        (date): Max date from database
    """
    sql_statement = '''select max(crash_date + interval '1' day) from {}.{};'''.format(schema_name, table_name)

    with engine.connect() as connection:
        result = connection.execute(sql_statement)
        for row in result:
            max_date = row[0]

        if max_date:
            return max_date
        else:
            return (date.today() - timedelta(days=5)).strftime('%Y-%m-%d')


def get_list_of_dates_to_process(start_date):
    """
    Function to list of dates to process

    Args:
        start_date(date): Starting date
    Returns:
        (date): List of dates from start date to yesterday's date
    """
    end_date = date.today() - timedelta(days=2)
    date_df = pd.date_range(start_date, end_date, freq='d')
    return date_df.strftime('%Y-%m-%d').to_list()


def read_data_for_crash_date(crash_date, api_url):
    """
    Function to read json data from API using requests library

    Args:
        crash_date(date): Date for which crashes data is fetched
        api_url(string): API endpoint for crashes data
    Returns:
        data(dict): Return the json response of API containing crashes data for that date
    """
    params = {'crash_date': crash_date}
    r = requests.get(url=api_url, params=params)

    # extracting data in json format
    data = r.json()
    return data


def get_data_df(data, column_list):
    """
    Function to convert json data to dataframe

    Args:
        data(dict): json response of API containing crashes data
        column_list(list): List containing key names to be processed from data dict
    Returns:
        df(Dataframe) : Dataframe containing collisions data
        collision_id_list_str(str) : A String of list of collision ids being processed needed so that
                        existing collision id records can be deleted from database before inserting them
                        to avoid duplicates in database
    """
    df = pd.json_normalize(data, sep='_')

    df = df.drop(columns=[col for col in df if col not in column_list])

    collision_id_list = df['collision_id'].tolist()

    collision_id_list_str = str(collision_id_list)[1:-1]

    return df, collision_id_list_str


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
    #Delete existing collision id records to ensure deduplication
    sql_statement = 'delete from {}.{} where collision_id in ({})'.format(schema_name, table_name,
                                                                          collision_id_list_str)
    engine.execute(sql_statement)
    df.to_sql(name=table_name, schema=schema_name, con=engine, if_exists='append', index=False)


if __name__ == '__main__':
    main()
