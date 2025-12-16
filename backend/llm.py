import ollama

llm = ollama.Client()

def generate(prompt):
    result = llm.generate(model="mistral:latest", prompt=prompt)
    return result.response