from flask import Flask, request, jsonify, Response
import requests
import json

app = Flask(__name__)

# Ollama's local server URL (you might need to change the port depending on your setup)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.route('/', methods=['POST'])
def generate():
    try:
        # Extract the JSON data from the incoming request
        data = request.get_json()
        
        # Validate that 'prompt' is present in the request data
        prompt = data.get('prompt', None)
        model = data.get('model', 'llama3.1')  # Default model to llama3.1 if not provided
        
        if not prompt:
            return jsonify({"error": "Prompt not provided"}), 400
        
        # Forward the request to the local Ollama API
        ollama_payload = {
            "model": model,
            "prompt": prompt,
            "stream": True  # Enable streaming
        }
        
        # Send the request to Ollama with streaming enabled
        response = requests.post(OLLAMA_API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(ollama_payload), stream=True)
        
        if response.status_code != 200:
            return jsonify({"error": f"Failed to generate text, status code: {response.status_code}"}), response.status_code
        
        # Stream the response from Ollama to the client
        def stream():
            for line in response.iter_lines():
                if line:
                    # Try to decode the JSON for each chunk
                    try:
                        json_data = json.loads(line.decode('utf-8'))
                        yield json.dumps(json_data) + '\n'  # Return each chunk as a separate JSON object
                    except json.JSONDecodeError:
                        yield json.dumps({"error": "Error decoding JSON from stream"}) + '\n'

        return Response(stream(), content_type='application/json')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
