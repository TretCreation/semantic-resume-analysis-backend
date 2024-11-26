import os
import re
from transformers import pipeline
from PyPDF2 import PdfReader
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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

def get_bert_features(text):
    embeddings = bert_pipeline(text)
    return np.mean(embeddings[0], axis=0)

def process_resumes(resumes_path):
    resumes = []
    for filename in os.listdir(resumes_path):
        if filename.endswith('.pdf'):
            filepath = os.path.join(resumes_path, filename)
            text = extract_text_from_pdf(filepath)
            resumes.append({
                "FileName": filename,
                "text": text,
                "bertFeatures": get_bert_features(text)
            })
    return resumes

def analyze_resumes(processed_resumes, criteria):
    criteria_text = " ".join(
        f"{criterion['skill']}" if "skill" in criterion else "" +
        f"{criterion['education']}" if "education" in criterion else "" +
        f"{criterion['language']}" if "language" in criterion else ""
        for criterion in criteria
    )
    
    criteria_features = get_bert_features(criteria_text)
    criteria_skills = [criterion["skill"] for criterion in criteria if "skill" in criterion]
    
    results = []
    for resume in processed_resumes:
        extracted_data = extract_data(resume["text"], criteria_skills)
        
        similarity_score = cosine_similarity(
            [resume["bertFeatures"]],
            [criteria_features]
        )[0][0]

        rating = 0
        for criterion in criteria:
            if "skill" in criterion and criterion["skill"] in extracted_data["skills"]:
                rating += 1
            if "totalExperience" in criterion and extracted_data["totalExperience"] >= criterion["totalExperience"]:
                rating += 1
            if "education" in criterion and criterion["education"] in extracted_data["education"]:
                rating += 1
            if "language" in criterion and criterion["language"] in extracted_data["languages"]:
                rating += 1

        results.append({
            "Rating": rating,
            "SimilarityScore": similarity_score,
            "FileName": resume["FileName"],
            "ExtractedData": extracted_data
        })

    results = sorted(results, key=lambda x: (x["Rating"], x["SimilarityScore"]), reverse=True)
    return results
