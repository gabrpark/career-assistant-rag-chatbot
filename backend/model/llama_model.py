from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Path to your model directory
model_directory = "/Users/gabrielpark/Downloads/llama-models-main/models/llama3_1/Meta-Llama-3.1-8B-Instruct"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_directory)
model = AutoModelForCausalLM.from_pretrained(model_directory)


def generate_response(question, context):
    input_text = question + " " + " ".join(context)
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    output = model.generate(input_ids, max_length=200)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response
