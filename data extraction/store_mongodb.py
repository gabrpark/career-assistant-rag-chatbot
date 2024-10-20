import os
import json
from pymongo import MongoClient

try:
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the fb_data.json file
    json_file_path = os.path.join(
        current_directory, 'fb_data_chatgpt_reformat.json')

    # Open and read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Debugging: Check if the JSON was loaded correctly
    # print("Data loaded from JSON:", data)

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['caDB']  # Replace with your DB name
    collection = db['fbGroupPosts']  # Replace with your collection name

    # Debugging: Check the MongoDB connection
    print("Connected to MongoDB")

    # Insert the 'post' directly into the collection
    result = collection.insert_one(data['data'][0])

    # Debugging: Check if the insertion was successful
    print(f"Data inserted with _id: {result.inserted_id}")

except Exception as e:
    print("An error occurred:", e)
