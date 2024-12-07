import os
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

ASTRA_BUNDLE_PATH = 'D:\\TaskL\\ecommerce\\fashion\\secure-connect-fashion.zip'
ASTRA_TOKEN = 'AstraCS:BKqgmBNxuNomJYKJdeGPMHsN:1193f2373e361ef650e14858658707de7d4f695ec126004c23ba70dfe46ecfc9'

ASTRA_KEYSPACE = 'catalog'

# Configuration for connecting to Astra DB
cloud_config = {
    'secure_connect_bundle': ASTRA_BUNDLE_PATH
}
auth_provider = PlainTextAuthProvider("token", ASTRA_TOKEN)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect(keyspace=ASTRA_KEYSPACE)

# Function to load data from Cassandra tables
def load_data_from_cassandra(session):
    # Load data from Customers table
    query_customers = "SELECT customerid, customername, cityid FROM Customers"
    rows_customers = session.execute(query_customers)
    customers = []
    for row in rows_customers:
        customers.append(row)

    # Load data from Cities table
    query_cities = "SELECT cityid, cityname, statename FROM Cities"
    rows_cities = session.execute(query_cities)
    cities = []
    for row in rows_cities:
        cities.append(row)

    return customers, cities

# Function to join tables and verify results
def join_and_verify_data(customers, cities):
    # Convert data to pandas DataFrames
    df_customers = pd.DataFrame(customers)
    df_cities = pd.DataFrame(cities)

    # Perform the join
    result = pd.merge(df_customers, df_cities, on='cityid', how='inner')

    # Select only the required columns
    result = result[['customername', 'cityname', 'statename']]

    return result

# Main function
def main():
    customers, cities = load_data_from_cassandra(session)
    result = join_and_verify_data(customers, cities)
    print(result)

# Execute the main function
if __name__ == "__main__":
    main()
