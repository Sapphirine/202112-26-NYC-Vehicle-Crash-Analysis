"""
Author : Shivam Ojha
Version : 1
Version Date : 15th Nov 2021
Description : This script is to preprocess the weather data from
https://www.wunderground.com/history/daily/us/ny/new-york-city/KJFK/
and load into postgres db
"""
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import os

def preprocess_weather_data(weather_df):
    """
    Pre process weather dataset

    Args:
        weather_df (dataframe): Dataframe with weather data
    """
    # make sure we have time objects
    weather_df['Date1'] = pd.to_datetime(weather_df['Date'])
    weather_df['Hour'] = pd.to_datetime(weather_df['Hour']).dt.strftime('%H:%M')
    weather_df['Datetime'] = pd.to_datetime(weather_df['Date1'].apply(str)+' '+weather_df['Hour'])
    del weather_df['Date1']

    # Delete duplicate values
    weather_df.drop_duplicates(inplace=True)

    # Drop values if NA
    print ("Dropping null values")
    weather_df['Hour'].dropna(inplace=True)
    weather_df['Date'].dropna(inplace=True)
    weather_df['Temp'].dropna(inplace=True)
    weather_df['Condition'].dropna(inplace=True)

    return weather_df


def main():
    """
    Script to preprocess the scraped weather data
    """
    print ("Script started at " + str(datetime.now()))

    # Initialise database parameters
    database_url = os.getenv('database_url')
    schema_name = 'weather'
    engine = create_engine(database_url, echo=False)
    weather_table = 'weather_data'
    weather_table_processed = 'weather_data_processed'

    sql_statement = '''select * from {}.{}'''.format(schema_name, weather_table)
    weather_df = pd.read_sql_query(sql_statement, database_url)

    weather_df = preprocess_weather_data(weather_df)

    #Update preprocessed table
    weather_df.to_sql(name=weather_table_processed, schema=schema_name, con=engine,
           if_exists='replace', index=False, method='multi')
    print ("Script completed at " + str(datetime.now()))

if __name__ == '__main__':
    main()
