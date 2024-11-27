import os
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('bert-base-uncased')

STOP_WORDS = {'i', 'a', 'the', 'and', 'of', 'to', 'in', 'is', 'with', 'for', 'on', 'by', 'an', 'at', 'it', 'as', 'from'}

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def preprocess_text(text):
    return ' '.join(text.split())

def extract_key_terms(text, top_n=5):
    words = text.split()
    word_freq = {word: words.count(word) for word in set(words) if word.lower() not in STOP_WORDS}
    sorted_terms = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return [term[0] for term in sorted_terms]

def extract_core_content(text, top_n=2):
    sentences = text.split('. ')
    embeddings = model.encode(sentences)
    avg_embedding = np.mean(embeddings, axis=0)
    similarities = cosine_similarity([avg_embedding], embeddings)[0]
    top_indices = similarities.argsort()[-top_n:][::-1]
    core_sentences = [sentences[i] for i in top_indices]
    return core_sentences

def extract_water_content(text, top_n=2):
    sentences = text.split('. ')
    embeddings = model.encode(sentences)
    avg_embedding = np.mean(embeddings, axis=0)
    similarities = cosine_similarity([avg_embedding], embeddings)[0]
    bottom_indices = similarities.argsort()[:top_n]
    water_sentences = [sentences[i] for i in bottom_indices]
    return water_sentences

def calculate_boringness(text):
    words = text.split()
    unique_words = set(words)
    boringness = (1 - len(unique_words) / len(words)) * 100  # Частка повторюваних слів у відсотках
    return round(boringness, 2)

def extract_stop_words(text):
    words = text.split()
    stop_words_in_text = [word for word in words if word.lower() in STOP_WORDS]
    return list(set(stop_words_in_text))

def analyze_resume_with_bert(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    preprocessed_text = preprocess_text(raw_text)
    
    key_terms = extract_key_terms(preprocessed_text)
    core_content = extract_core_content(preprocessed_text)
    water_content = extract_water_content(preprocessed_text)
    boringness = calculate_boringness(preprocessed_text)
    stop_words = extract_stop_words(preprocessed_text)
    
    total_words = len(preprocessed_text.split())
    
    return {
        "key_terms": key_terms,
        "core_content": core_content,
        "water_content": water_content,
        "boringness": boringness,
        "stop_words": stop_words,
        "total_words": total_words
    }

def analyze_dataset_with_bert(dataset_dir):
    results = {}
    for file_name in os.listdir(dataset_dir):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(dataset_dir, file_name)
            results[file_name] = analyze_resume_with_bert(file_path)
    return results

def save_results_to_file(results, output_file="result.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        for file_name, analysis in results.items():
            f.write(f"========================================\n")
            f.write(f"Файл: {file_name}\n")
            f.write(f"Ключові терміни: {analysis['key_terms']}\n")
            f.write(f"Ядро тексту: {'. '.join(analysis['core_content'])}\n")
            f.write(f"Вода: {'. '.join(analysis['water_content'])}\n")
            f.write(f"Нудність тексту: {analysis['boringness']}%\n")
            f.write(f"Стоп-слова: {analysis['stop_words']}\n")
            f.write(f"Кількість слів: {analysis['total_words']}\n")
            f.write(f"========================================\n\n")

dataset_dir = '../dataset/resumes'  # Шлях до каталогу
results = analyze_dataset_with_bert(dataset_dir)
save_results_to_file(results)
print("Результати збережено у файлі result.txt")
