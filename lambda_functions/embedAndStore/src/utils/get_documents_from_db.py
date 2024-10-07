import boto3
# import json
import re

from utils.config import S3_BUCKET

s3_client = boto3.client('s3')

# Function to chunk text with overlap
def chunk_document(text, chunk_size=200, overlap=50):
    words = re.findall(r'\S+|\n', text)  # \S+ matches non-whitespace chars, includes punctuation
    chunks = []
    i = 0
    
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunk_text = ' '.join(chunk)
        chunks.append(chunk_text)
        i += chunk_size - overlap  # Move window by chunk_size - overlap
        
    return chunks
    
# Function to retrieve and chunk documents from S3 based on a filename prefix
def get_documents_from_db(filename_prefix):
    # List objects in the S3 bucket that match the filename prefix
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=filename_prefix)
    
    documents = []
    if 'Contents' in response:
        for obj in response['Contents']:
            document_key = obj['Key']
            # Fetch the object content from S3
            s3_object = s3_client.get_object(Bucket=S3_BUCKET, Key=document_key)
            document_text = s3_object['Body'].read().decode('utf-8')
            
            # Chunk the document text with overlap
            chunks = chunk_document(document_text, chunk_size=200, overlap=50)
            documents.extend(chunks)
    
    return documents