'''
Author : Animesh Bhasin
Version : 1
Version Date : 16th Nov 2022
Description : This script is to load the crashes.csv data into postgres db
'''


import pandas as pd
from sqlalchemy import create_engine
import os

df = pd.read_csv('/Users/animeshbhasin/Downloads/Motor_Vehicle_Collisions_-_Crashes.csv')
engine = create_engine(os.getenv('database_url'), echo=False)
df.to_sql('crashes_full', schema='crash', con=engine, if_exists='append', index=True, index_label='index')
