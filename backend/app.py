from flask import Flask, request, jsonify
from model.llama_model import generate_response
from utils.pdf_utils.py import extract_text_from_pdf
from utils.retrieval_utils.py import retrieve_relevant_chunks, split_text_into_chunks

app = Flask(__name__)

# Load and prepare the PDF data
pdf_path = 'data/how-to-win-friends-and-influence-people.pdf'
book_text = extract_text_from_pdf(pdf_path)
chunks = split_text_into_chunks(book_text)


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    question = data['question']
    relevant_chunks = retrieve_relevant_chunks(question, chunks)
    response = generate_response(question, relevant_chunks)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
