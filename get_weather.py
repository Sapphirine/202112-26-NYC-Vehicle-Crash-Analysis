"""
Author : Shivam Ojha
Version : 3.1
Version Date : 15th Dec 2021
Description : This script is to scrape the weather data from
https://www.wunderground.com/history/daily/us/ny/new-york-city/KJFK/
and load into postgres db
"""
import re
import datetime
from datetime import date
import requests
import pandas as pd
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import os

HISTORICAL_DATA_FLG = False

def format_data(given_date, api_key):
    """Get relevant data from the wunderground request call

    Args:
        given_date (str): Date string
        api_key (str): API key from website

    Returns:
        transposed_object: Dictionary of lists with weather values every hour
    """
    given_date = datetime.datetime.strptime(given_date, '%Y-%m-%d').strftime('%Y%m%d')
    url = f'https://api.weather.com/v1/location/KJFK:9:US/observations/historical.json?apiKey={api_key}&units=e&startDate={given_date}&endDate={given_date}'
    response = requests.get(url).json()
    mappings = {'Hour': 'hour', "Date": 'date', 'Temp': 'temp',
                'Dew': 'dewPt', 'humidity': 'rh', 'Wind Cardinal': 'wdir_cardinal',
                'Wind Speed': 'wspd', 'Wind Gust': 'gust', 'Pressure List': 'pressure',
                'Precip Rate': 'precip_hrly', 'Condition': 'wx_phrase'}
    formatted_object = []
    try:
        for tuple1 in response['observations']:
            timestamp = tuple1['valid_time_gmt']
            given_date = datetime.datetime.fromtimestamp(timestamp)
            tuple1['date'] = given_date.strftime("%d %b %Y")
            tuple1['hour'] = given_date.strftime("%I:%M %p")
            formatted_tuple = {}
            for element in mappings.keys():
                formatted_tuple[element] = tuple1[mappings[element]] if tuple1[mappings[element]] else 0
            formatted_object.append(formatted_tuple)
        transposed_object = {}

        for element in mappings.keys():
            temp_list = []
            for tuple in formatted_object:
                temp_list.append(tuple[element])
            transposed_object[element] = temp_list
        return transposed_object
    except KeyError:
        return None

def generate_dates(yesterday_date):
    """Generate dates for historical load

    Args:
        yesterday_date (date object): date yesterday

    Returns:
        dates_list: List of dates to fetch the weather data
    """
    days_in_month = {1: 31, 2: 28, 3: 31, 4: 30,
                  5: 31, 6: 30, 7: 31, 8: 31,
                  9: 30, 10: 31, 11: 30, 12: 31}
    days_in_month_leap = {1: 31, 2: 29, 3: 31, 4: 30,
                  5: 31, 6: 30, 7: 31, 8: 31,
                  9: 30, 10: 31, 11: 30, 12: 31}
    dates_list = []
    for year in range(2012, 2022):
        for month in range(1, 13):
            if year % 4 == 0:
                day_cnt = days_in_month_leap[month]
            else:
                day_cnt = days_in_month[month]
            for day in range(1, day_cnt+1):
                date_str = "{}-{}-{}".format(year, month, day)
                date_object = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                if date_object > yesterday_date:
                    break
                dates_list.append(date_str)
    return dates_list


def get_api_key(link):
    """Get the API key from wunderground

    Args:
        link (str): website link

    Returns:
        api_key: API key
    """
    response = requests.get(link)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    scrp = soup.find_all('script', id="app-root-state")
    str1 = 'SUN_API_KEY&q;:&q;'
    res1 = re.findall(str1+'(.*)', str(scrp))
    api_key = res1[0].split('&q;')[0]
    return api_key


def generate_incremental_dates(given_date):
    """Generate dates for incremental load of weather data

    Args:
        given_date (str): maximum date from database

    Returns:
        dates: list of dates
    """
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    today_obj = datetime.datetime.strptime(today_str, "%Y-%m-%d")
    dates = []
    dates.append(given_date)
    date_obj = datetime.datetime.strptime(given_date, "%Y-%m-%d")
    while date_obj < today_obj:
        date_obj = date_obj + datetime.timedelta(days=1)
        date_str = date_obj.strftime("%Y-%m-%d")
        dates.append(date_str)
    return dates


def get_date_max_date_in_db(engine, schema_name, table_name):
    """Get maximum date value from the database

    Args:
        engine : postgres engine to connect to db
        schema_name (str): schema name
        table_name (str): table name

    Returns:
        max_date: Maximum date in the database
    """
    sql_statement = '''select max({}."Date") from {}.{};'''.format(table_name,
                                                                    schema_name,
                                                                    table_name)
    with engine.connect() as connection:
        result = connection.execute(sql_statement)
        for row in result:
            max_date = row[0]
    return max_date


def write_to_db(df_, table_name, schema_name, engine, date_str):
    """Function to insert dataframe values to database

    Args:
        df_ (dataframe object): Dataframe with weather data
        table_name (str): table name
        schema_name (str): schema name
        engine : postgres engine to connect to db
        date_str (str): date string
    """
    sql_statement = '''delete from {}.{} where {}."Date" in ('{}')'''.format(schema_name, 
                    table_name, table_name, date_str)
    engine.execute(sql_statement)
    df_.to_sql(name=table_name, schema=schema_name, con=engine,
                if_exists='append', index=False, method='multi')

def main():
    """Main function
    """
    # Get the api key from wunderground
    link = 'https://www.wunderground.com'
    api_key = get_api_key(link)

    # Database credentials
    database_url = os.getenv('database_url')
    schema_name = 'weather'
    weather_table_name = 'weather_data'
    engine = create_engine(database_url, echo=False)

    yesterday = date.today() - datetime.timedelta(days=1)
    yes_date_str = yesterday.strftime("%Y-%m-%d")
    yesterday_obj = datetime.datetime.strptime(yes_date_str, "%Y-%m-%d")

    if HISTORICAL_DATA_FLG:
        #load data from 2012 to now
        dates = generate_dates(yesterday_obj)
    else:
        #load incremental data, compared to last date in db
        max_date = get_date_max_date_in_db(engine, schema_name, weather_table_name)
        dates = generate_incremental_dates(str(max_date))
    for date1 in dates:
        df_ = pd.DataFrame(format_data(date1, api_key))
        if isinstance(df_, pd.core.frame.DataFrame):
            df_['Date'] = date1
            df_['station'] = 'KJFK'
            print("Storing values for date: {}".format(date1))

            write_to_db(df_, table_name= weather_table_name,
                        schema_name = schema_name,
                        engine= engine, date_str=date1)


if __name__ == '__main__':
    main()
