import requests
import json

url = "https://only-supreme-cub.ngrok-free.app/"
headers = {"Content-Type": "application/json"}

data = {
    "model": "llama3.1",
    "prompt": "Hi, how are you?",
}

# Make the POST request and stream the response
response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)

# Variable to accumulate the response chunks
generated_text = ""

# Check if the response status code is 200
if response.status_code == 200:
    # Iterate over the streamed response line by line
    for line in response.iter_lines():
        if line:
            try:
                # Decode the line and load it as JSON
                json_data = json.loads(line.decode('utf-8'))
                
                # Append the response to the generated_text
                generated_text += json_data.get("response", "")
                
                # Print each chunk (optional for debugging)
                print(f"Received chunk: {json_data.get('response', '')}")
                
                # If the "done" flag is True, stop receiving further chunks
                if json_data.get("done", False):
                    print("Generation completed.")
                    break
            except json.JSONDecodeError:
                print("Error decoding JSON from the response.")
    
    # Print the complete generated text as a human-readable sentence
    print("\nGenerated Text:")
    print(generated_text)
else:
    print(f"Error: Received status code {response.status_code}")
