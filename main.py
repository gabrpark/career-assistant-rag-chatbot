import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the variables
group_id = os.getenv('GROUP_ID')
access_token = os.getenv('ACCESS_TOKEN')

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

# To fetch a limited number of posts
# posts = get_group_posts(group_id, access_token, limit=3)


# To fetch all available posts (no limit)
posts = get_group_posts(group_id, access_token)

if posts is None:
    print("Failed to retrieve posts. Please check your group ID and access token.")
elif 'data' not in posts:
    print("No posts found or an error occurred.")
else:
    for post in posts['data']:
        post_id = post.get('id', 'No ID')
        message = post.get('message', None)

        if message:
            print(f"Post ID: {post_id}")
            print(f"Post: {message}")

            comments = get_post_comments(
                post_id, access_token) if post_id != 'No ID' else {}
            if comments and 'data' in comments:
                for comment in comments['data']:
                    comment_id = comment.get('id', 'No ID')
                    comment_message = comment.get('message', 'No message')
                    print(f"Comment: {comment_message}")

                    # Fetch and print replies to the comment
                    replies = get_comment_replies(comment_id, access_token)
                    if replies and 'data' in replies:
                        for reply in replies['data']:
                            reply_message = reply.get('message', 'No message')
                            print(f"  Reply: {reply_message}")
                    else:
                        print("  No replies found")
            else:
                print("No comments found")
        else:
            print(f"Post ID: {post_id} has no content")
