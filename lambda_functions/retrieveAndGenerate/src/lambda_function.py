import json
import boto3
# from utils.prompt_helper import create_prompt
from utils.generate_embeddings import generate_embeddings
from utils.config import PINECONE_API_KEY, PINECONE_API_ENV
from utils.build_prompt import build_prompt
from utils.generate_response_from_bedrock import generate_response_from_bedrock
from pinecone import Pinecone

# Initialize Bedrock client
# bedrock_client = boto3.client('bedrock-runtime', region_name='us-west-2')

# Create Pinecone instance
pc = Pinecone(api_key=PINECONE_API_KEY)

INDEX_NAME = 'my-second-index'

# Lambda handler
def lambda_handler(event, context):
    user_query = event.get('user_query', '')

    if not user_query:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'No user query provided'})
        }

    # Generate query embedding
    query_embedding = generate_embeddings(user_query)
    
    # Connect to the Pinecone index
    index = pc.Index(INDEX_NAME)

    # Query Pinecone with the generated embedding
    query_response = index.query(vector=query_embedding, top_k=5, include_metadata=True)
    
    # Extract relevant chunks from Pinecone results
    relevant_chunks = [
        match['metadata']['text']
        for match in query_response['matches']
    ]

    # Create the prompt using user query and the relevant chunks
    prompt = build_prompt(user_query, relevant_chunks)

    # # Prepare the payload for the model invocation
    # native_request = {
    #     "prompt": formatted_prompt,
    #     "max_gen_len": 512,
    #     "temperature": 0.5,
    # }

    # # Invoke the Bedrock model
    model_response = generate_response_from_bedrock(prompt)

    return {
        'statusCode': 200,
        'body': json.dumps({'generated_text': model_response})
    }
    
    # Return relevant chunks as the response
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps({
    #         'relevant_chunks': relevant_chunks
    #     })
    # }