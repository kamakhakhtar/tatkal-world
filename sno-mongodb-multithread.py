from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

# MongoDB connection string
url = "mongodb+srv://desktop:__logiTech2022@idcreation.suwlqzk.mongodb.net/?retryWrites=true&w=majority"

def process_collection(db_name, collection_name):
    # Create a new client and connect to the server
    client = MongoClient(url)
    db = client[db_name]
    collection = db[collection_name]
    documents = collection.find({})
    sno_counter = 1
    for document in documents:
        # Add 'sno' field to the document
        document['sno'] = sno_counter
        sno_counter += 1
        print(f"Adding sno {document['sno']} to document with id {document['_id']} in collection {collection_name}")
        # Update the document in the collection with the new 'sno' field
        collection.update_one({'_id': document['_id']}, {'$set': document})

if __name__ == "__main__":
    # Create a new client and connect to the server
    client = MongoClient(url)
    
    # Get the list of all databases in the MongoDB cluster
    databases = client.list_database_names()
    print(databases)
    exit()
    # Create a ThreadPoolExecutor with max_workers set to the number of concurrent tasks you want to run
    max_workers = 5  # You can adjust this based on your system's capabilities
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Iterate through each database
        for db_name in databases:
            # Get the database object
            db = client[db_name]

            # Get the list of all collections in the current database
            collections = db.list_collection_names()

            # Submit tasks for processing each collection concurrently
            for collection_name in collections:
                executor.submit(process_collection, db_name, collection_name)
