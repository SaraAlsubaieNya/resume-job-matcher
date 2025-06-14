import sqlite3
import pandas as pd
from sqlalchemy import create_engine
import os

class DatabaseManager:
    def __init__(self, db_path="data/resume_matcher.db"):
        db_dir = os.path.dirname(db_path)
        if db_dir:  # Only create directory if it's not empty
           os.makedirs(db_dir, exist_ok=True)
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.init_tables()
    
    
    def init_tables(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Resumes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE,
                content TEXT,
                processed_content TEXT,
                skills TEXT,
                experience TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Job descriptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_descriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                company TEXT,
                content TEXT,
                processed_content TEXT,
                required_skills TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Matches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER,
                job_id INTEGER,
                similarity_score REAL,
                rank_position INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (resume_id) REFERENCES resumes (id),
                FOREIGN KEY (job_id) REFERENCES job_descriptions (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_resume(self, filename, content, processed_content="", skills="", experience=""):
        """Insert resume into database"""
        df = pd.DataFrame([{
            'filename': filename,
            'content': content,
            'processed_content': processed_content,
            'skills': skills,
            'experience': experience
        }])
        df.to_sql('resumes', self.engine, if_exists='append', index=False)
    
    def insert_job(self, title, company, content, processed_content="", required_skills=""):
        """Insert job description into database"""
        df = pd.DataFrame([{
            'title': title,
            'company': company,
            'content': content,
            'processed_content': processed_content,
            'required_skills': required_skills
        }])
        df.to_sql('job_descriptions', self.engine, if_exists='append', index=False)
    
    def get_resumes(self):
        """Get all resumes"""
        return pd.read_sql('SELECT * FROM resumes', self.engine)
    
    def get_jobs(self):
        """Get all job descriptions"""
        return pd.read_sql('SELECT * FROM job_descriptions', self.engine)
    def close(self):
        """Close the database connection"""
        if hasattr(self, 'engine') and self.engine:
            self.engine.dispose()