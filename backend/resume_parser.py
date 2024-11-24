import os
import re
from transformers import pipeline
from PyPDF2 import PdfReader

bert_pipeline = pipeline("feature-extraction", model="bert-base-uncased")

def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_data(text, criteria_skills):
    skills_regex = '|'.join(criteria_skills)
    skills = re.findall(rf'\b({skills_regex})\b', text, re.IGNORECASE)
    
    languages = re.findall(r'\b(English|German|Spanish)\b', text, re.IGNORECASE)

    education = re.findall(r'\b(Bachelor|Master|PhD)\b', text, re.IGNORECASE)

    experience_matches = re.findall(r'(\w+\s\d{4})\s*-\s*(\w+\s\d{4}|till date)', text)

    total_experience = 0
    for start, end in experience_matches:
        start_year = int(re.search(r'\d{4}', start).group())
        end_year = int(re.search(r'\d{4}', end).group()) if 'till date' not in end else 2024
        total_experience += (end_year - start_year) * 12

    return {
        "skills": list(set(skills)),
        "languages": list(set(languages)),
        "education": list(set(education)),
        "totalExperience": total_experience
    }

def process_resumes(resumes_path):
    resumes = []
    for filename in os.listdir(resumes_path):
        if filename.endswith('.pdf'):
            filepath = os.path.join(resumes_path, filename)
            text = extract_text_from_pdf(filepath)
            resumes.append({
                "FileName": filename,
                "text": text
            })
    return resumes

def analyze_resumes(processed_resumes, criteria):
    criteria_skills = [criterion["skill"] for criterion in criteria if "skill" in criterion]
    
    results = []

    for resume in processed_resumes:
        extracted_data = extract_data(resume["text"], criteria_skills)
        rating = 0

        for criterion in criteria:
            if "skill" in criterion:
                if criterion["skill"] in extracted_data["skills"]:
                    rating += 1
            
            if "totalExperience" in criterion:
                if extracted_data["totalExperience"] >= criterion["totalExperience"]:
                    rating += 1
            
            if "education" in criterion:
                if criterion["education"] in extracted_data["education"]:
                    rating += 1
            
            if "language" in criterion:
                if criterion["language"] in extracted_data["languages"]:
                    rating += 1

        result = {
            "Rating": rating,
            "FileName": resume["FileName"],
            "ExtractedData": extracted_data
        }
        results.append(result)

    results = sorted(results, key=lambda x: x["Rating"], reverse=True)
    return results
