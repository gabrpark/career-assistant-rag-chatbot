import requests
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# Get the variables
group_id = os.getenv('GROUP_ID_2')
access_token = os.getenv('ACCESS_TOKEN')
mongo_uri = os.getenv('MONGO_URI')
mongo_db_name = os.getenv('MONGO_DB_NAME')

# Initialize MongoDB client
client = MongoClient(mongo_uri)
db = client[mongo_db_name]

# Fetch group posts with an optional limit


def get_group_posts(group_id, access_token, limit=None):
    url = f'https://graph.facebook.com/{group_id}/feed'
    params = {
        'access_token': access_token
    }
    if limit is not None:
        params['limit'] = limit
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        handle_error(response)
        return None

# Fetch comments for a specific post


def get_post_comments(post_id, access_token):
    url = f'https://graph.facebook.com/{post_id}/comments'
    params = {
        'access_token': access_token
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        handle_error(response)
        return None

# Fetch replies for a specific comment


def get_comment_replies(comment_id, access_token):
    url = f'https://graph.facebook.com/{comment_id}/comments'
    params = {
        'access_token': access_token
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        handle_error(response)
        return None

# Error handling function


def handle_error(response):
    try:
        error_message = response.json().get('error', {}).get('message', 'Unknown error')
    except ValueError:
        error_message = 'Unknown error'
    print(f"Error {response.status_code}: {error_message}")

# Function to save data into MongoDB


def save_to_mongodb(collection_name, data):
    collection = db[collection_name]
    collection.insert_one(data)


# To fetch all available posts (no limit)
posts = get_group_posts(group_id, access_token)

if posts is None:
    print("Failed to retrieve posts. Please check your group ID and access token.")
elif 'data' not in posts:
    print("No posts found or an error occurred.")
else:
    # Updated section to handle missing fields
    for post in posts['data']:
        post_id = post.get('id', 'No ID')
        message = post.get('message', None)
        created_time = post.get('created_time', 'No time available')
        author_id = post.get('from', {}).get('id', 'No Author ID')

        if message:
            post_data = {
                '_id': post_id,
                'message': message,
                'created_time': created_time,
                'author_id': id,
                'comments': []
            }
            print(f"Post ID: {post_id}")
            print(f"Post: {message}")
            print(f"Created Time: {created_time}")
            print(f"Author ID: {id}")

            comments = get_post_comments(
                post_id, access_token) if post_id != 'No ID' else {}
            if comments and 'data' in comments:
                for comment in comments['data']:
                    comment_id = comment.get('id', 'No ID')
                    comment_message = comment.get('message', 'No message')
                    comment_created_time = comment.get(
                        'created_time', 'No time available')
                    comment_author_id = comment.get(
                        'from', {}).get('id', 'No Author ID')

                    comment_data = {
                        '_id': comment_id,
                        'message': comment_message,
                        'created_time': comment_created_time,
                        'author_id': comment_author_id,
                        'replies': []
                    }
                    post_data['comments'].append(comment_data)

                    print(f"Comment: {comment_message}")
                    print(f"Created Time: {comment_created_time}")
                    print(f"Author ID: {comment_author_id}")

                    # Fetch and print replies to the comment
                    replies = get_comment_replies(comment_id, access_token)
                    if replies and 'data' in replies:
                        for reply in replies['data']:
                            reply_message = reply.get('message', 'No message')
                            reply_created_time = reply.get(
                                'created_time', 'No time available')
                            reply_id = reply.get('id', 'No ID')
                            reply_author_id = reply.get(
                                'from', {}).get('id', 'No Author ID')

                            reply_data = {
                                '_id': reply_id,
                                'message': reply_message,
                                'created_time': reply_created_time,
                                'author_id': reply_author_id
                            }
                            comment_data['replies'].append(reply_data)

                            print(f"  Reply: {reply_message}")
                            print(f"  Created Time: {reply_created_time}")
                            print(f"  Author ID: {reply_author_id}")
                    else:
                        print("  No replies found")
            else:
                print("No comments found")
            save_to_mongodb('facebookPosts', post_data)
        else:
            print(f"Post ID: {post_id} has no content")
