# Function to build the prompt
def build_prompt(user_query, relevant_chunks):
    prompt = "The following are relevant pieces of information:\n\n"
    
    for idx, chunk in enumerate(relevant_chunks):
        prompt += f"Chunk {idx + 1}: {chunk}\n\n"
    
    prompt += f"Now, based on the above information, answer the following question:\n\nUser Query: {user_query}\n"
    
    return prompt