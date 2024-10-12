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

    # Modify the prompt to request structured JSON response and optimized code
    query = f"""
    Provide a detailed time and space complexity analysis of the following code in JSON format. 
    The JSON object should include "timeComplexity" with "bestCase", "averageCase", "worstCase" keys, "spaceComplexity", 
    "summary", and suggest optimized code if possible.

    Code:
    {code_input}

    Respond only with valid JSON. Here is an example structure:
    {{
        "timeComplexity": {{
            "bestCase": "O(1)",
            "averageCase": "O(n)",
            "worstCase": "O(n^2)"
        }},
        "spaceComplexity": "O(n)",
        "summary": "The code runs efficiently, Uses additional space proportional to input size."
    }}
    """

    # Call the AI model to generate content
    response = model.generate_content(query)

    # Debug: print the raw response from the model
    print("Raw Response from AI Model:", response)

    if response and response._result and response._result.candidates:
        # Extract the JSON part from the content
        json_text = response._result.candidates[0].content.parts[0].text.strip()

        # Remove the Markdown code block formatting
        json_text = json_text.replace("```json", "").replace("```", "").strip()

        try:
            # Attempt to parse the JSON output
            analysis_json = json.loads(json_text)

            # Additional logging for structure
            print("Parsed JSON:", analysis_json)

            # Check for required keys
            if 'timeComplexity' in analysis_json and 'spaceComplexity' in analysis_json:
                return jsonify(analysis_json)
            else:
                return jsonify({"error": "Missing expected fields in the response."}), 500

        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)  # Log the error for debugging
            print("Response was:", json_text)  # Log the raw response
            return jsonify({"error": "Invalid JSON response from the model."}), 500
    else:
        print("No valid candidates found in response.")  # Log the error
        return jsonify({"error": "Could not analyze the code."}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
