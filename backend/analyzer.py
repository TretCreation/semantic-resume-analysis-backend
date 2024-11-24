from flask import Flask, request, jsonify
from resume_parser import process_resumes, analyze_resumes

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        criteria = request.json.get('criteria', [])
        
        resumes_path = '../dataset/resumes'
        processed_resumes = process_resumes(resumes_path)
        
        results = analyze_resumes(processed_resumes, criteria)
        
        return jsonify({
            "message": "Analysis completed successfully",
            "candidates": results
        })
    except Exception as e:
        return jsonify({
            "message": "An error occurred while analyzing resumes.",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
