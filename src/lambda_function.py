import json
import boto3
# import pinecone
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from botocore.exceptions import ClientError
# For S3-based document retrieval
from utils.get_documents_from_db import get_documents_from_db
from utils.generate_embeddings import generate_embeddings
from dotenv import load_dotenv

# Initialize the Bedrock client
# Update region if necessary
bedrock_client = boto3.client('bedrock-runtime', region_name='us-west-2')

# Initialize a client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create a serverless index
index_name = "example-index"
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=2,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
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
        chunk_embeddings = [generate_embeddings(
            chunk) for chunk in document_chunks]

        # Upsert the embeddings into Pinecone (vector storage)
        vectors = []
        for i, embedding in enumerate(chunk_embeddings):
            vectors.append({
                'id': f'vector_{i}',
                'values': embedding
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
