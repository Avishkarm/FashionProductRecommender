import os
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Define the path to the CSV file
CSV_PATH = 'D:\\TaskL\\ecommerce\\fashion\\cities.csv'

# Read environment variables
secure_connect_bundle_path = os.getenv('ASTRA_DB_SECURE_CONNECT_BUNDLE', 'D:\\TaskL\\ecommerce\\fashion\\secure-connect-fashion.zip')
application_token = os.getenv('ASTRA_DB_TOKEN', 'AstraCS:BKqgmBNxuNomJYKJdeGPMHsN:1193f2373e361ef650e14858658707de7d4f695ec126004c23ba70dfe46ecfc9')

# Define the keyspace
ASTRA_KEYSPACE = 'catalog'

# Ensure the secure connect bundle and token are correctly read
print(f"Secure connect bundle path: {secure_connect_bundle_path}")
print(f"Application token: {application_token}")

# Configuration for connecting to Astra DB
cloud_config = {
    'secure_connect_bundle': secure_connect_bundle_path
}
auth_provider = PlainTextAuthProvider("token", application_token)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect(keyspace=ASTRA_KEYSPACE)

# Function to insert data into the Cities table
def insert_data_into_cities(session, cities_data):
    insert_query = "INSERT INTO Cities (cityid, cityname,StateId,StateName) VALUES (%s, %s,%s,%s)"
    
    for _, row in cities_data.iterrows():
        print(f"Inserting row: {row}")  # Debug statement to show the row being inserted
        session.execute(insert_query, (row['CityId'], row['CityName'],row['StateId'],row['StateName']))  # Insert both cityid and cityname
    
    print("Data inserted successfully")

# Function to load data from Cassandra tables
def load_data_from_cassandra(session):
    query_cities = "SELECT * FROM catalog.Cities"
    rows_cities = session.execute(query_cities)
    cities = []
    for row in rows_cities:
        cities.append(row)
    
    return cities

# Main function
def main():
    # Read the CSV file into a DataFrame
    try:
        cities_data = pd.read_csv(CSV_PATH)
        print("CSV data read successfully:")
        print(cities_data.head())  # Display the first few rows to verify the data
        print("Columns in CSV file:", cities_data.columns)  # Display column names
    except FileNotFoundError:
        print(f"Error: File not found at path {CSV_PATH}")
        return
    
    # Insert data into the Cities table
    insert_data_into_cities(session, cities_data)
    
    # Load and print data from Cassandra to verify
    cities = load_data_from_cassandra(session)
    print("Data loaded from Cassandra:")
    for city in cities:
        print(city)

# Execute the main function
if __name__ == "__main__":
    main()
