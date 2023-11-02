import pandas as pd
from pymongo import MongoClient

# MongoDB connection parameters
mongo_host = 'localhost'
mongo_port = 27017
database_name = 'unverify25oct'     
collection_name = 'unverify'

 # mongo db
url = "mongodb+srv://tempsmsadmin:m0W1Rirs6pKJ1eri@cluster0.hfly6u2.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(url)

db = client[database_name]
collection = db[collection_name]

# Retrieve data from MongoDB collection
data = list(collection.find({}))

# Convert MongoDB data to DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV file
csv_filename = f'{database_name}_{collection_name}.csv'
df.to_csv(csv_filename, index=False)

print(f'Data has been exported to {csv_filename}')