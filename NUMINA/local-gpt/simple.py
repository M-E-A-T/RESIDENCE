import ollama

client = ollama.Client()

model = "llama2"  # Replace model name
prompt = "What is Python?"

req = client.generate(model=model, prompt=prompt)

print("Response from Ollama:")
print(req.response)
