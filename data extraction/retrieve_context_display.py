from pymongo import MongoClient
from datetime import datetime
import pprint

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["caDB"]  # Replace with your MongoDB database
collection = db["fbGroupPosts"]  # Replace with your MongoDB collection

# Function to format the timestamp


def format_time(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M")

# Recursive function to format comments and nested replies


def format_comments(comment_data, file, indent=0):
    for comment in comment_data:
        created_time = format_time(comment.get("created_time", ""))
        message = comment.get("message", "")
        author = comment.get("author", "Unknown Author")
        file.write(f"{' ' * indent}Author: {author}\n")
        file.write(f"{' ' * indent}Time: {created_time}\n")
        file.write(f"{' ' * indent}Message: {message}\n\n")

        # Check if this comment has nested replies (comments inside comments)
        if "comments" in comment and "data" in comment["comments"]:
            format_comments(comment["comments"]["data"], file, indent + 4)

# Function to retrieve and store posts in a text file


def store_posts_in_file(filename):
    posts = collection.find()  # Retrieve all posts from the collection
    post_count = 0

    with open(filename, 'w', encoding='utf-8') as file:
        for post in posts:
            post_count += 1
            print(f"Processing post {post_count}")

            # Check if 'data' key exists in the post document
            if 'data' in post:
                for item in post['data']:  # Accessing 'data' array inside the post
                    created_time = format_time(item.get("created_time", ""))
                    message = item.get("message", "")
                    author = item.get("author", "Unknown Author")

                    # Write the main post to file
                    file.write(f"Post by: {author}\n")
                    file.write(f"Time: {created_time}\n")
                    file.write(f"Message: {message}\n\n")

                    # Write comments on the post, if any
                    if "comments" in item and "data" in item["comments"]:
                        file.write("Comments:\n")
                        format_comments(
                            item["comments"]["data"], file, indent=4)
                    file.write("-" * 50 + "\n")
            else:
                print(f"No 'data' found in post {post_count}")

    print(f"Processed {post_count} posts")


# Call the function to store posts and comments in the file
store_posts_in_file("output.txt")
