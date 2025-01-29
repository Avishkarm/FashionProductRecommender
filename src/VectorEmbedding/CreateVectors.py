from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Path to your Secure Connect Bundle
secure_connect_bundle_path = '<Your secure-connect-keyspace.zip'

# Your application token
application_token = 'Yourtoken'

# Setup authentication provider
auth_provider = PlainTextAuthProvider('token', application_token)

# Connect to the Cassandra database using the secure connect bundle
cluster = Cluster(
    cloud={"secure_connect_bundle": secure_connect_bundle_path},
    auth_provider=auth_provider
)
session = cluster.connect()

# Define keyspace
keyspace = "catalog"
v_dimension = 5

# Set the keyspace
session.set_keyspace(keyspace)

# Verify connection by querying the system.local table
rows = session.execute("SELECT release_version FROM system.local")
for row in rows:
    print(f"Connected to Cassandra, release version: {row.release_version}")

# Print the current keyspace
current_keyspace = session.execute("SELECT keyspace_name FROM system_schema.keyspaces WHERE keyspace_name = %s", [keyspace])
for row in current_keyspace:
    print(f"Connected to keyspace: {row.keyspace_name}")

print("Connected to AstraDB and keyspace successfully!")

session.execute((
    "CREATE TABLE IF NOT EXISTS {keyspace}.ProductImageVectors (ProductId INT PRIMARY KEY, ProductDesc TEXT, ImageURL text, ProductImageVector VECTOR<FLOAT,{v_dimension}>);"
).format(keyspace=keyspace, v_dimension=v_dimension))

session.execute((
    "CREATE CUSTOM INDEX IF NOT EXISTS idx_ProductImageVectors "
    "ON {keyspace}.ProductImageVectors "
    "(ProductImageVector) USING 'StorageAttachedIndex' WITH OPTIONS = "
    "{{'similarity_function' : 'cosine'}};"
).format(keyspace=keyspace))

text_blocks = [
    (1, "Under colors of Benetton Men White Boxer Trunks","UndercolorsofBenetton-Men-White-Boxer_b4ef04538840c0020e4829ecc042ead1_images.jpg", [-0.0711570307612419, 0.0490173473954201, -0.0348679609596729, -0.0208837632089853, 0.0250527486205101]
),
    (2, "Turtle Men Check Red Shirt","Turtle-Men-Check-Red-Shirt_4982b2b1a76a85a85c9adc8b4b2d523a_images.jpg" ,[-0.0678209140896797, 0.0918413251638412, 0.0087888557463884, -0.0005505480221473, 0.0586152337491512]),
    (3, "United Colors of Benetton Men White Check Shirt","United-Colors-of-Benetton-Men-White-Check-Shirt_13cfaff26872c298112a8e7da15c1e1d_images.jpg" ,[-0.0697127357125282, 0.0486216545104980, -0.0169006455689669, -0.0160229168832302, 0.0137890130281448]
),
 (4, "United Colors of Benetton Men Check White Shirts","UnitedColorsofBenetton-Men-Check-White-Shirts_5bd8cae4fc61052a6f00cfcd69c4a936_images.jpg" ,[-0.0499644242227077, 0.0566278323531151, -0.0294290613383055, -0.0070271748118103, 0.0289674568921328]
),
    (5, "Wrangler-Men-Broad-Blue-Shirt","Wrangler-Men-Broad-Blue-Shirt_8211520250143786-1.jpg" ,[-0.0581886917352676, 0.0378338471055031, 0.0425588376820087, -0.0423909239470959, 0.0186673272401094]
)
]
for block in text_blocks:
    id, text, text,vector = block
    session.execute(
        f"INSERT INTO {keyspace}.ProductImageVectors(ProductId, ProductDesc, ImageURL,ProductImageVector) VALUES (%s, %s,%s, %s)",
        (id, text, text,vector)
    )

ann_query = (
    f"SELECT  ProductDesc, ImageURL,similarity_cosine(ProductImageVector, [0.15, 0.1, 0.1, 0.35, 0.55]) as similarity FROM {keyspace}.ProductImageVectors "
    "ORDER BY ProductImageVector ANN OF [0.15, 0.1, 0.1, 0.35, 0.55] LIMIT 2"
)
for row in session.execute(ann_query):
    print(f"[{row.productdesc}\" (sim: {row.similarity:.4f})")

    # Print success message
    
print("Data with semantic match.")

ann_query_matching = (
    f"SELECT  ProductDesc, ImageURL,similarity_cosine(ProductImageVector, [-0.0499644242227077, 0.0566278323531151, -0.0294290613383055, -0.0070271748118103, 0.0289674568921328]) as similarity FROM {keyspace}.ProductImageVectors "
    "ORDER BY ProductImageVector ANN OF [-0.0499644242227077, 0.0566278323531151, -0.0294290613383055, -0.0070271748118103, 0.0289674568921328] LIMIT 2"
)
for row in session.execute(ann_query_matching):
    print(f"[{row.productdesc}\" (sim: {row.similarity:.4f})")
    
print("Data with similar match.")

