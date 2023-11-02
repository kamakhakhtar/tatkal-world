from pymongo import MongoClient

# MongoDB connection string
url = "mongodb+srv://desktop:__logiTech2022@idcreation.suwlqzk.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(url)

# Get the list of all databases in the MongoDB cluster
databases = client.list_database_names()

# Iterate through each database
for db_name in databases:
    # Get the database object
    db = client[db_name]
    
    # Get the list of all collections in the current database
    collections = db.list_collection_names()
    
    # Iterate through each collection in the current database
    for collection_name in collections:
        # Get the collection object
        collection = db[collection_name]
        print(collection_name)
        # Retrieve all documents from the collection
        documents = collection.find({})
        
        # Get the total number of documents in the collection
        # total_documents = documents.count()
        
        # Update documents with 'sno' field
        sno_counter = 1
        for document in documents:
            # Add 'sno' field to the document
            document['sno'] = sno_counter
            sno_counter += 1
            print(f"adding sno {sno_counter}, id = {document['_id']} , uname = {document['username']}")
            # Update the document in the collection with the new 'sno' field
            collection.update_one({'_id': document['_id']}, {'$set': document})
