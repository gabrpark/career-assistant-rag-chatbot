import json
import boto3
from pinecone import Pinecone, ServerlessSpec
from botocore.exceptions import ClientError
from utils.get_documents_from_db import get_documents_from_db  # For S3-based document retrieval
from utils.generate_embeddings import generate_embeddings  # For S3-based document retrieval
from utils.config import PINECONE_API_KEY, PINECONE_API_ENV

# Initialize the Bedrock client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-west-2')  # Update region if necessary

# Create Pinecone instance
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check if the index already exists, if not, create it
index_name = 'my-second-index'

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1024,  # Adjust dimension to your embeddings model
        metric='cosine',  # Choose appropriate metric (e.g., cosine, euclidean)
        spec=ServerlessSpec(
            cloud='aws',  # Choose the cloud provider
            region=PINECONE_API_ENV  # Pass your Pinecone environment
        )
    )
    
# Wait for the index to be ready
while not pc.describe_index(index_name).status['ready']:
    time.sleep(1)
    
index = pc.Index(index_name)
def lambda_handler(event, context):
    filename_prefix = 'test'

    try:
        # Retrieve relevant documents from S3 and chunk them
        document_chunks = get_documents_from_db(filename_prefix)
        
        # Generate embeddings for each chunk
        chunk_embeddings = [generate_embeddings(chunk) for chunk in document_chunks]

        # Upsert the embeddings into Pinecone (vector storage)
        vectors = []
        for i, (embedding, chunk) in enumerate(zip(chunk_embeddings, document_chunks)):
            vectors.append({
                'id': f'vector_{i}',
                'values': embedding,
                'metadata': {
                    'text': chunk,  # Store the document chunk as metadata
                    'document_id': filename_prefix,  # You can add more metadata like document ID
                    'chunk_id': i  # Optionally store chunk ID for reference
                }
            })

        # Upsert vectors into Pinecone index
        index.upsert(vectors=vectors)
        print(index.describe_index_stats())
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Embeddings upserted successfully into Pinecone'})
        }

    except ClientError as e:
        print(f"ClientError: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }