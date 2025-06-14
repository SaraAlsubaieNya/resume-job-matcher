import pytest
import pandas as pd
from src.nlp.text_processor import TextProcessor
from src.utils.database import DatabaseManager
from src.data_fetchers.job_scraper import JobScraper

class TestTextProcessor:
    def setup_method(self):
        self.processor = TextProcessor()
    
    def test_clean_text(self):
        text = "Hello World! 123 #test"
        cleaned = self.processor.clean_text(text)
        assert cleaned == "hello world test"
    
    def test_extract_skills(self):
        text = "I have experience with Python, JavaScript, and SQL databases"
        skills = self.processor.extract_skills(text)
        assert "python" in skills
        assert "javascript" in skills
        assert "sql" in skills
    
    def test_calculate_similarity(self):
        text1 = "Python developer with Django experience"
        text2 = "Looking for Python programmer with web framework knowledge"
        similarity = self.processor.calculate_similarity(text1, text2)
        assert 0 <= similarity <= 1
        assert similarity > 0.5  # Should be reasonably similar

class TestDatabase:
    def setup_method(self):
        self.db = DatabaseManager("test.db")
    
    def test_database_creation(self):
        # Test that tables are created
        resumes = self.db.get_resumes()
        jobs = self.db.get_jobs()
        assert isinstance(resumes, pd.DataFrame)
        assert isinstance(jobs, pd.DataFrame)
    
    def teardown_method(self):
    # Close the database connection first
        if hasattr(self, 'db') and self.db:
            self.db.close()
    
    # Clean up test database
        import os
        if os.path.exists("test.db"):
           try:
              os.remove("test.db")
           except PermissionError:
              pass  # Ignore if we can't delete it

class TestJobScraper:
    def setup_method(self):
        self.scraper = JobScraper()
    
    def test_create_sample_jobs(self):
        jobs = self.scraper.create_sample_jobs()
        assert len(jobs) > 0
        assert 'title' in jobs.columns
        assert 'company' in jobs.columns
        assert 'content' in jobs.columns