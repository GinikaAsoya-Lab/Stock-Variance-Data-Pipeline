import sqlite3
import pandas as pd
import os

# 1. Create a connection to a new SQLite database file
db_name = 'hospitality_stock.db'
conn = sqlite3.connect(db_name)

# 2. Load the CSV files into Pandas DataFrames
print("Reading CSV files from synthetic_data folder...")
outlets_df = pd.read_csv('synthetic_data/dim_outlets.csv')
products_df = pd.read_csv('synthetic_data/dim_products.csv')
facts_df = pd.read_csv('synthetic_data/fact_stock_movements.csv')

# 3. Write the data into the SQLite database as tables
print("Building database tables...")
outlets_df.to_sql('dim_outlets', conn, if_exists='replace', index=False)
products_df.to_sql('dim_products', conn, if_exists='replace', index=False)
facts_df.to_sql('fact_stock_movements', conn, if_exists='replace', index=False)

conn.close()
print(f"Success! Database '{db_name}' has been created with all your tables.")