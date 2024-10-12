from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables from the .env file
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Initialize Flask app
app = Flask(__name__)

# Home route to render the UI
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to analyze code
@app.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.json
    code_input = data.get('code')

    # Check if code input is provided
    if not code_input:
        return jsonify({"error": "No code provided."}), 400

    # Modify the prompt to request structured JSON response
    query = f"""
    Provide a detailed time and space complexity analysis of the following code in JSON format. 
    The JSON object should include "timeComplexity" with "bestCase", "averageCase", "worstCase" keys, "spaceComplexity", and "summary".

    Code:
    {code_input}

    Respond only with valid JSON.
    """
    
    # Call the AI model to generate content
    response = model.generate_content(query)

    # Debug: print the raw response from the model
    #print("Raw Response from AI Model:", response)

    # Use _result instead of result
    if response and response._result and response._result.candidates:
        # Extract the JSON part from the content
        json_text = response._result.candidates[0].content.parts[0].text.strip()

        # Remove the Markdown code block formatting
        json_text = json_text.replace("```json", "").replace("```", "").strip()

        try:
            # Attempt to parse the JSON output
            analysis_json = json.loads(json_text)
            return jsonify(analysis_json)
        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)  # Log the error for debugging
            return jsonify({"error": "Invalid JSON response from the model."}), 500
    else:
        return jsonify({"error": "Could not analyze the code."}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
