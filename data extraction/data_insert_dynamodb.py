import boto3
import uuid
import json
import os

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('fbGroupPosts')


def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)


def insert_item_to_dynamodb(data):
    """Insert an item into DynamoDB with a UUID."""
    for item in data['data']:
        # Generate a unique UUID for each post
        post_id = str(uuid.uuid4())

        # Structure the data as per DynamoDB format
        dynamo_item = {
            'post_id': post_id,
            'created_time': item['created_time'],
            'author': item['author'],
            'message': item['message'],
            'comments': item.get('comments', {})  # Adding comments if present
        }

        # Insert the item into DynamoDB
        response = table.put_item(Item=dynamo_item)
        print(f"Inserted item with post_id: {post_id}, response: {response}")


if __name__ == "__main__":
    # Specify the path to your JSON file
    # Replace with the path to your JSON file
    # file_path = 'fb_data_chatgpt_reformat.json'

    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the fb_data.json file
    json_file_path = os.path.join(
        current_directory, 'fb_data_chatgpt_reformat.json')

    # Load the data from the JSON file
    data = load_json(json_file_path)

    # Insert the data into DynamoDB
    insert_item_to_dynamodb(data)
