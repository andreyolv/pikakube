#%% Libraries
import os
import pandas as pd
from sqlalchemy import create_engine
from getpass import getpass

# %% Variables
base = os.getcwd()
path_tables = os.path.join(base, 'tables')
tables = os.listdir(path_tables)
password = getpass('Database password:')

#%% Create database connection
con = create_engine(f'postgresql+psycopg2://postgres:{password}@localhost:5432/postgres')

#%% Upload tables
for table in tables:
    path_table = os.path.join(path_tables, table)
    table = table.replace('.csv', '')
    df = pd.read_csv(path_table)
    df.to_sql(
        table, con, schema='transactional',
        if_exists='replace', index=False
    )
    print(f'Table {table} uploaded!')