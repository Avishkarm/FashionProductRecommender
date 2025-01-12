import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# setx ASTRA_DB_SECURE_CONNECT_BUNDLE "D:\TaskL\ecommerce\fashion\FashionRecommenderApp\astra-db-recommendations-starter\SCB\secure-connect-fashion.zip"

# setx ASTRA_DB_TOKEN "AstraCS:ZlyMyCobxWSafNzEERRFGkJt:b8190d55067628fcadb3e4224afbfb92327cb33590d8ddb955f0718d86b4d1bf"

# Read environment variables
secure_connect_bundle_path = os.getenv('ASTRA_DB_SECURE_CONNECT_BUNDLE')
application_token = os.getenv('ASTRA_DB_TOKEN')

# Debug prints to check environment variables
print(f"Secure Connect Bundle Path: {secure_connect_bundle_path}")
print(f"Application Token: {application_token}")

# Check if the environment variables are loaded correctly
if not secure_connect_bundle_path or not os.path.exists(secure_connect_bundle_path):
    raise FileNotFoundError(f"Secure connect bundle not found at path: {secure_connect_bundle_path}")

if not application_token:
    raise ValueError("Application token not found in environment variables")

# Connect to the Cassandra database using the secure connect bundle
session = Cluster(
    cloud={"secure_connect_bundle": secure_connect_bundle_path},
    auth_provider=PlainTextAuthProvider("token", application_token),
).connect()

# Define keyspace and vector dimension
keyspace = "catalog"
v_dimension = 5

session.execute((
    "CREATE TABLE IF NOT EXISTS {keyspace}.ProductDescVectors (ProductId INT PRIMARY KEY, ProductDesc TEXT, ProductDescVector VECTOR<FLOAT,{v_dimension}>);"
).format(keyspace=keyspace, v_dimension=v_dimension))

session.execute((
    "CREATE CUSTOM INDEX IF NOT EXISTS idx_ProductDescVectors "
    "ON {keyspace}.ProductDescVectors "
    "(ProductDescVector) USING 'StorageAttachedIndex' WITH OPTIONS = "
    "{{'similarity_function' : 'cosine'}};"
).format(keyspace=keyspace))

text_blocks = [
    (1, "Under colors of Benetton Men White Boxer Trunks", [-0.0711570307612419, 0.0490173473954201, -0.0348679609596729, -0.0208837632089853, 0.0250527486205101]
),
    (2, "Turtle Men Check Red Shirt", [-0.0678209140896797, 0.0918413251638412, 0.0087888557463884, -0.0005505480221473, 0.0586152337491512]),
    (3, "United Colors of Benetton Men White Check Shirt", [-0.0697127357125282, 0.0486216545104980, -0.0169006455689669, -0.0160229168832302, 0.0137890130281448]
),
 (4, "United Colors of Benetton Men Check White Shirts", [-0.0499644242227077, 0.0566278323531151, -0.0294290613383055, -0.0070271748118103, 0.0289674568921328]
),
    (5, "Wrangler Men Broad Blue Shirt", [-0.0581886917352676, 0.0378338471055031, 0.0425588376820087, -0.0423909239470959, 0.0186673272401094]
),
]
for block in text_blocks:
    id, text, vector = block
    session.execute(
        f"INSERT INTO {keyspace}.ProductDescVectors(ProductId, ProductDesc, ProductDescVector) VALUES (%s, %s, %s)",
        (id, text, vector)
    )

ann_query = (
    f"SELECT  ProductDesc, similarity_cosine(ProductDescVector, [0.15, 0.1, 0.1, 0.35, 0.55]) as similarity FROM {keyspace}.ProductDescVectors "
    "ORDER BY ProductDescVector ANN OF [0.15, 0.1, 0.1, 0.35, 0.55] LIMIT 2"
)
for row in session.execute(ann_query):
    print(f"[{row.productdesc}\" (sim: {row.similarity:.4f})")

    # Print success message
    
print("Data with semantic match.")

ann_query_matching = (
    f"SELECT  ProductDesc, similarity_cosine(ProductDescVector, [-0.0499644242227077, 0.0566278323531151, -0.0294290613383055, -0.0070271748118103, 0.0289674568921328]) as similarity FROM {keyspace}.ProductDescVectors "
    "ORDER BY ProductDescVector ANN OF [-0.0499644242227077, 0.0566278323531151, -0.0294290613383055, -0.0070271748118103, 0.0289674568921328] LIMIT 2"
)
for row in session.execute(ann_query_matching):
    print(f"[{row.productdesc}\" (sim: {row.similarity:.4f})")
    
print("Data with similar match.")

