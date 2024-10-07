import json
import boto3

bedrock_client = boto3.client('bedrock-runtime', region_name='us-west-2')

# Function to generate response using Bedrock (Llama3.2 model)
def generate_response_from_bedrock(prompt):
    response = bedrock_client.invoke_model(
        modelId='meta.llama3-1-8b-instruct-v1:0',  # Specify correct modelId
        contentType='application/json',
        body=json.dumps({
            "prompt": prompt,
            "max_gen_len": 500,  # Adjust based on your needs
            "temperature": 0.7  # Optional: adjust the response randomness
        })
    )
    
    # Extract the result from the Bedrock response
    response_body = response['body'].read().decode('utf-8')
    model_response = json.loads(response_body)
    return model_response
    
    # # Invoke the Bedrock model
    # response = bedrock_client.invoke_model(
    #     modelId='meta.llama3-1-8b-instruct-v1:0',
    #     body=json.dumps(native_request)
    # )