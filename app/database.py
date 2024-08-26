from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client['rag_chatbot']


def get_post_by_id(post_id):
    return db.posts.find_one({"post_id": post_id})


def save_post(post_data):
    db.posts.insert_one(post_data)
