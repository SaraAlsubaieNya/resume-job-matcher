import re
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import os

# Download required NLTK data
def download_nltk_data():
    """Download all required NLTK data"""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab')
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

# Download data when module is imported
download_nltk_data()

class TextProcessor:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize TextProcessor with CI/CD support"""
        self.stop_words = set(stopwords.words('english'))
        self.model = None
        
        # Check if running in CI/CD environment
        is_ci = os.getenv('CI') or os.getenv('GITLAB_CI') or os.getenv('MOCK_MODEL')
        
        if is_ci:
            print("Running in CI/CD environment - using mock model")
            self.model = None
        else:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(model_name)
                print(f"Loaded SentenceTransformer model: {model_name}")
            except Exception as e:
                print(f"Failed to load SentenceTransformer: {e}")
                print("Continuing with basic text processing only")
                self.model = None
        
        # Initialize spaCy
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def clean_text(self, text):
        """Clean and preprocess text"""
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = ' '.join(text.split())
        
        return text
    
    def extract_skills(self, text):
        """Extract technical skills from text"""
        skills_patterns = [
            r'\b(?:python|java|javascript|c\+\+|c#|php|ruby|go|rust|kotlin|swift)\b',
            r'\b(?:react|angular|vue|django|flask|spring|express|nodejs)\b',
            r'\b(?:sql|mysql|postgresql|mongodb|redis|elasticsearch)\b',
            r'\b(?:aws|azure|gcp|docker|kubernetes|jenkins|git)\b',
            r'\b(?:machine learning|deep learning|ai|nlp|computer vision)\b',
            r'\b(?:tensorflow|pytorch|scikit-learn|pandas|numpy)\b'
        ]
        
        skills = set()
        text_lower = text.lower()
        
        for pattern in skills_patterns:
            matches = re.findall(pattern, text_lower)
            skills.update(matches)
        
        return list(skills)
    
    def preprocess_text(self, text):
        """Complete text preprocessing with error handling"""
        try:
            # Clean text
            cleaned = self.clean_text(text)
            
            # Tokenize with fallback
            try:
                tokens = word_tokenize(cleaned)
            except LookupError:
                # Fallback to simple split if NLTK fails
                tokens = cleaned.split()
            
            # Remove stopwords
            tokens = [token for token in tokens if token not in self.stop_words]
            
            # Join back
            processed = ' '.join(tokens)
            
            return processed
            
        except Exception as e:
            print(f"Error in text preprocessing: {e}")
            # Return cleaned text as fallback
            return self.clean_text(text)
    
    def get_embeddings(self, texts):
        """Get sentence embeddings"""
        if self.model is None:
            # Return mock embeddings for CI/CD or when model unavailable
            if isinstance(texts, str):
                texts = [texts]
            # Return random embeddings for testing
            return np.random.rand(len(texts), 384)  # 384 is dimension of all-MiniLM-L6-v2
        
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(texts)
        return embeddings
    
    def calculate_similarity(self, text1, text2):
        """Calculate cosine similarity between two texts"""
        if self.model is None:
            # Return mock similarity for CI/CD
            # Use simple text overlap as fallback
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            if not words1 or not words2:
                return 0.0
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            return float(intersection / union) if union > 0 else 0.0
        
        embeddings = self.get_embeddings([text1, text2])
        
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )
        
        return float(similarity)