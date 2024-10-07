# Use the official AWS Lambda Python 3.12 base image
FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY src/ .

# Command to run the Lambda function (this is required for Lambda container images)
CMD [ "lambda_function.lambda_handler"]