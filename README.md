# Facebook Group Data Pipeline & RAG System

A system for extracting Facebook group content, processing it with embeddings, and implementing a retrieval-augmented generation (RAG) chat system using AWS Bedrock Llama2.

## Project Structure

```
├── data extraction/
│   ├── data_extractor.py               # Facebook data extraction script
│   ├── data_extractor_store_mongo.py   # MongoDB storage integration
│   ├── data_insert_dynamodb.py         # DynamoDB storage integration
│   ├── store_mongodb.py                # MongoDB utilities
│   ├── get_post_dynamodb.py            # DynamoDB retrieval
│   ├── retrieve_context_display.py     # Context display utilities
│   ├── fb_data.json                    # Raw Facebook data
│   ├── fb_data_chatgpt_reformat.json   # Reformatted data
│   ├── test.json                       # Test data
│   ├── post_details.txt                # Post details log
│   └── index.html                      # Web interface
├── lambda_functions/
│   ├── embedAndStore/
│   │   ├── PineconeLayer/             # Pinecone dependencies
│   │   ├── src/
│   │   │   ├── lambda_function.py     # Main embedding function
│   │   │   └── utils/
│   │   │       ├── config.py          # Configuration settings
│   │   │       ├── generate_embeddings.py    # Embedding generation
│   │   │       └── get_documents_from_db.py  # Database retrieval
│   │   └── template.yml               # SAM template
│   └── retrieveAndGenerate/
│       ├── PineconeLayer/             # Pinecone dependencies
│       ├── src/
│       │   ├── lambda_function.py     # Main retrieval function
│       │   └── utils/
│       │       ├── build_prompt.py    # Prompt engineering
│       │       ├── config.py          # Configuration settings
│       │       ├── find_most_similar_chunks.py    # Similarity search
│       │       ├── generate_embeddings.py         # Embedding utilities
│       │       └── generate_response_from_bedrock.py  # LLM integration
│       └── template.yml               # SAM template
├── myenv/                             # Python virtual environment
├── requirements.txt                   # Project dependencies
└── README.md                          # Project documentation
```

## System Overview

This system provides an end-to-end pipeline for:
1. Extracting data from Facebook groups
2. Storing data in MongoDB and DynamoDB
3. Generating embeddings using AWS Bedrock Titan
4. Storing vectors in Pinecone
5. Retrieving relevant context and generating responses using Llama2

## Prerequisites

- Python 3.8+
- Facebook Developer Account and Access Token
- AWS Account with access to:
  - Bedrock (Titan & Llama2)
  - DynamoDB
  - Lambda
  - SAM CLI
- MongoDB Atlas account
- Pinecone account

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/facebook-rag-system.git

# Create and activate virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Set up environment variables:
```plaintext
# .env file
FACEBOOK_ACCESS_TOKEN=your_token
MONGODB_URI=your_mongodb_uri
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
PINECONE_API_KEY=your_pinecone_key
```

2. Configure AWS credentials:
```bash
aws configure
```

## Data Extraction

```bash
# Extract Facebook data
python data_extraction/data_extractor.py

# Store in MongoDB
python data_extraction/data_extractor_store_mongo.py

# Store in DynamoDB
python data_extraction/data_insert_dynamodb.py
```

## Lambda Function Deployment

### Embedding and Storage Function
```bash
cd lambda_functions/embedAndStore
sam build
sam deploy --guided
```

### Retrieval and Generation Function
```bash
cd lambda_functions/retrieveAndGenerate
sam build
sam deploy --guided
```

## Usage

### Data Extraction
```python
from data_extraction.data_extractor import FacebookDataExtractor

extractor = FacebookDataExtractor()
posts = extractor.extract_group_posts()
```

### Database Operations
```python
from data_extraction.store_mongodb import MongoDBHandler

db = MongoDBHandler()
db.store_posts(posts)
```

### Web Interface
1. Start the local server:
```bash
python -m http.server 8000
```
2. Open `http://localhost:8000/data_extraction/index.html`

## Lambda Functions

### embedAndStore
- Processes documents from database
- Generates embeddings using Bedrock Titan
- Stores vectors in Pinecone

### retrieveAndGenerate
- Receives user queries
- Finds similar content using Pinecone
- Generates responses using Llama2

## Error Handling

The system includes error handling for:
- Facebook API rate limits
- Database connection issues
- AWS service failures
- Invalid input data

## Monitoring

- CloudWatch Logs for Lambda functions
- MongoDB Atlas monitoring
- Pinecone metrics dashboard

## Development

```bash
# Run tests
pytest

# Format code
black .

# Lint code
flake8
```

## Security

- Use IAM roles for AWS services
- Rotate API keys regularly
- Encrypt sensitive data
- Implement authentication
- Regular security audits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Support

For support, please open an issue in the GitHub repository or contact [your-email@example.com]