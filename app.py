import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# You would need to set this in your .env file
API_KEY = os.getenv("LLM_API_KEY")
API_URL = os.getenv("LLM_API_URL", "https://api.mistral.ai/v1/chat/completions")
MODEL = os.getenv("LLM_MODEL", "mistral-medium")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        question = data.get('question', '')

        if not question:
            return jsonify({"error": "No question provided"}), 400

        if not API_KEY:
            return jsonify({
                "answer": "API key not configured. Please set the LLM_API_KEY in your .env file.",
                "error": True
            })

        # Prepare the prompt with ethical framing
        prompt = f"""You are a thoughtful and ethical AI assistant specializing in data privacy, surveillance, and AI ethics. 
        Your task is to respond to the following question in a clear, concise, and balanced manner:
        Question: {question}

        Please provide a well-informed and accessible answer (maximum 3–4 paragraphs) that:
        - Explains the ethical and privacy-related aspects of the issue.
        - Presents multiple perspectives (e.g., legal, societal, technological).
        - Offers real-world examples or references where relevant.
        - Avoids overly technical language and maintains a neutral, informative tone.

        Your goal is to help users think critically about ethical implications while respecting different viewpoints."""

        # Call external LLM API with Mistral API format
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        # Format for Mistral API (similar to OpenAI)
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are an ethical AI assistant focusing on privacy and ethics questions."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        
        # Process the response
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            return jsonify({"answer": answer})
        else:
            # Handle API errors with more detailed information
            error_message = f"Error calling Mistral AI service: {response.status_code}"
            
            # Provide more helpful information for common error codes
            if response.status_code == 401:
                error_message = "Authentication error: The API key was rejected. Please check your Mistral API key."
            elif response.status_code == 403:
                error_message = "Authorization error: Your API key doesn't have permission to use this model."
            elif response.status_code == 429:
                error_message = "Rate limit exceeded: Too many requests to the Mistral API."
            
            # Try to get more error details from the response if available
            try:
                error_details = response.json()
                if "error" in error_details and "message" in error_details["error"]:
                    error_message += f" - {error_details['error']['message']}"
            except:
                pass  # If we can't parse the error JSON, just use the status code message
                
            print(f"API Error: {error_message}")
            
            return jsonify({
                "answer": error_message,
                "error": True
            })
            
    except Exception as e:
        return jsonify({"answer": f"An error occurred: {str(e)}", "error": True})

if __name__ == '__main__':
    app.run(debug=True)
