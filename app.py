from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.json
    code_input = data.get('code')

    if not code_input:
        return jsonify({"error": "No code provided."}), 400

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
        "spaceComplexity": {{
            "bestCase": "O(1)",
            "averageCase": "O(n)",
            "worstCase": "O(n^2)"
        }},
        "summary": "The code runs efficiently, Uses additional space proportional to input size."
    }}
    """

    response = model.generate_content(query)

    print("Raw Response from AI Model:", response)

    if response and response._result and response._result.candidates:

        json_text = response._result.candidates[0].content.parts[0].text.strip()
        json_text = json_text.replace("```json", "").replace("```", "").strip()

        try:
            analysis_json = json.loads(json_text)

            print("Parsed JSON:", analysis_json)

            if 'timeComplexity' in analysis_json and 'spaceComplexity' in analysis_json:
                return jsonify(analysis_json)
            else:
                return jsonify({"error": "Missing expected fields in the response."}), 500

        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)
            print("Response was:", json_text)
            return jsonify({"error": "Invalid JSON response from the model."}), 500
    else:
        print("No valid candidates found in response.")
        return jsonify({"error": "Could not analyze the code."}), 500

if __name__ == '__main__':
    app.run(debug=True)
