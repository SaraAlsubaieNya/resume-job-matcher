import os
import pandas as pd
from docx import Document
import PyPDF2


class ResumeParser:
    def __init__(self, resume_folder="data/resumes/"):
        self.resume_folder = resume_folder
        os.makedirs(resume_folder, exist_ok=True)
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""
    
    def extract_text_from_docx(self, docx_path):
        """Extract text from DOCX file"""
        try:
            doc = Document(docx_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error reading DOCX {docx_path}: {e}")
            return ""
    
    def extract_text_from_txt(self, txt_path):
        """Extract text from TXT file"""
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading TXT {txt_path}: {e}")
            return ""
    
    def parse_resume(self, file_path):
        """Parse resume based on file extension"""
        filename = os.path.basename(file_path)
        extension = os.path.splitext(filename)[1].lower()
        
        if extension == '.pdf':
            content = self.extract_text_from_pdf(file_path)
        elif extension == '.docx':
            content = self.extract_text_from_docx(file_path)
        elif extension == '.txt':
            content = self.extract_text_from_txt(file_path)
        else:
            print(f"Unsupported file format: {extension}")
            return None
        
        return {
            'filename': filename,
            'content': content,
            'file_path': file_path
        }
    
    def parse_all_resumes(self):
        """Parse all resumes in the folder"""
        resumes = []
        for filename in os.listdir(self.resume_folder):
            if filename.lower().endswith(('.pdf', '.docx', '.txt')):
                file_path = os.path.join(self.resume_folder, filename)
                resume_data = self.parse_resume(file_path)
                if resume_data:
                    resumes.append(resume_data)
        
        return pd.DataFrame(resumes)