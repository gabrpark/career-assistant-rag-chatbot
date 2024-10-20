import boto3
import json
import os

# Initialize DynamoDB
# Ensure the correct region
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
# Replace with your actual DynamoDB table name
table = dynamodb.Table('fbGroupPosts')


def get_post_from_dynamodb(post_id, created_time):
    """Get a post by post_id and created_time from DynamoDB."""
    try:
        # Query DynamoDB with both partition key (post_id) and sort key (created_time)
        response = table.get_item(Key={
            'post_id': post_id,
            'created_time': created_time
        })
        return response.get('Item', None)  # Return the item if found
    except Exception as e:
        print(f"Error fetching item: {e}")
        return None


def format_post(post):
    """Format the post in a well-readable string."""
    if not post:
        return "Post not found."

    # Prepare formatted string output
    formatted_post = []
    formatted_post.append("Post Details:")
    formatted_post.append(f"Author: {post.get('author', 'N/A')}")
    formatted_post.append(f"Created Time: {post.get('created_time', 'N/A')}")
    formatted_post.append("\nMessage:")
    formatted_post.append(post.get('message', 'N/A'))

    # Handle comments
    comments = post.get('comments', {}).get('data', [])
    if comments:
        formatted_post.append("\nComments:")
        for i, comment in enumerate(comments, 1):
            formatted_post.append(f"\nComment {i}:")
            formatted_post.append(f"  Author: {comment.get('author', 'N/A')}")
            formatted_post.append(
                f"  Created Time: {comment.get('created_time', 'N/A')}")
            formatted_post.append(
                f"  Message: {comment.get('message', 'N/A')}")

            # Handle nested replies within a comment
            nested_comments = comment.get('comments', {}).get('data', [])
            if nested_comments:
                formatted_post.append("  Replies:")
                for j, reply in enumerate(nested_comments, 1):
                    formatted_post.append(f"    Reply {j}:")
                    formatted_post.append(
                        f"      Author: {reply.get('author', 'N/A')}")
                    formatted_post.append(f"      Created Time: {
                                          reply.get('created_time', 'N/A')}")
                    formatted_post.append(
                        f"      Message: {reply.get('message', 'N/A')}")
    else:
        formatted_post.append("\nNo comments available.")

    # Return formatted post as a single string
    return "\n".join(formatted_post)


def save_to_txt(file_path, content):
    """Save the formatted content to a text file."""
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"Post details saved to {file_path}")


if __name__ == "__main__":
    # Specify the post_id and created_time you want to retrieve
    # Replace with the actual post_id
    post_id = '87c39215-f3b7-45b1-93df-a7ac54011a48'
    created_time = '2024-10-11T22:16:00Z'  # Replace with the actual created_time

    # Fetch the post from DynamoDB
    post = get_post_from_dynamodb(post_id, created_time)

    # Format the post as a readable string
    formatted_post = format_post(post)

    # Print the formatted post to the console
    print(formatted_post)

    # Save the formatted post to a text file
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the output txt file
    txt_file_path = os.path.join(current_directory, 'post_details.txt')

    # Save the formatted post to a text file
    save_to_txt(txt_file_path, formatted_post)
