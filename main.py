import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the variables
group_id = os.getenv('GROUP_ID')
access_token = os.getenv('ACCESS_TOKEN')

# Fetch group posts


def get_group_posts(group_id, access_token):
    url = f'https://graph.facebook.com/{group_id}/feed'
    params = {
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    return response.json()

# Fetch comments for a specific post


def get_post_comments(post_id, access_token):
    url = f'https://graph.facebook.com/{post_id}/comments'
    params = {
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    return response.json()

# Fetch replies for a specific comment


def get_comment_replies(comment_id, access_token):
    url = f'https://graph.facebook.com/{comment_id}/comments'
    params = {
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    return response.json()


posts = get_group_posts(group_id, access_token)

for post in posts.get('data', []):
    post_id = post.get('id', 'No ID')
    message = post.get('message', None)

    if message:
        print(f"Post ID: {post_id}")
        print(f"Post: {message}")

        comments = get_post_comments(
            post_id, access_token) if post_id != 'No ID' else {}
        if 'data' in comments:
            for comment in comments['data']:
                comment_id = comment.get('id', 'No ID')
                comment_message = comment.get('message', 'No message')
                print(f"Comment: {comment_message}")

                # Fetch and print replies to the comment
                replies = get_comment_replies(comment_id, access_token)
                if 'data' in replies:
                    for reply in replies['data']:
                        reply_message = reply.get('message', 'No message')
                        print(f"  Reply: {reply_message}")
                else:
                    print("  No replies found")
        else:
            print("No comments found")
    else:
        print(f"Post ID: {post_id} has no content")
