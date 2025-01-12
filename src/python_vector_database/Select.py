import re
import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from getpass import getpass

# ASTRA_BUNDLE_PATH = 'D:\\TaskL\\ecommerce\\fashion\\secure-connect-fashion.zip'
# ASTRA_TOKEN='AstraCS:BKqgmBNxuNomJYKJdeGPMHsN:1193f2373e361ef650e14858658707de7d4f695ec126004c23ba70dfe46ecfc9'

# Read environment variables
secure_connect_bundle_path = os.getenv('ASTRA_DB_SECURE_CONNECT_BUNDLE')
application_token = os.getenv('ASTRA_DB_TOKEN')

# Define keyspace and vector dimension
ASTRA_KEYSPACE = 'catalog'
#keyspace = "catalog"

v_dimension = 5

cloud_config = {
    'secure_connect_bundle': secure_connect_bundle_path
}
# Connect to the Cassandra database using the secure connect bundle
# session = Cluster(
#     cloud={"secure_connect_bundle": secure_connect_bundle_path},
#     auth_provider=PlainTextAuthProvider("token", application_token),
# ).connect()
cluster = Cluster(cloud=cloud_config, auth_provider=PlainTextAuthProvider("token", application_token))
session = cluster.connect(keyspace=ASTRA_KEYSPACE)

# Function to load data from Cassandra tables
def load_data_from_cassandra(session):
    query_customers = "SELECT * FROM catalog.Cities"
    rows_customers = session.execute(query_customers)
    customers = []
    for row in rows_customers:
        customers.append(row)

    return customers

# Main function
def main():
    customers = load_data_from_cassandra(session)
    print(customers)

# Execute the main function
if __name__ == "__main__":
    main()
