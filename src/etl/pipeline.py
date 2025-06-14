import pandas as pd
from src.utils.database import DatabaseManager
from src.data_fetchers.resume_parser import ResumeParser
from src.data_fetchers.job_scraper import JobScraper
from src.nlp.text_processor import TextProcessor
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETLPipeline:
    def __init__(self):
        self.db = DatabaseManager()
        self.resume_parser = ResumeParser()
        self.job_scraper = JobScraper()
        self.text_processor = TextProcessor()
    
    def extract_resumes(self):
        """Extract resume data"""
        logger.info("Extracting resumes...")
        resumes_df = self.resume_parser.parse_all_resumes()
        logger.info(f"Extracted {len(resumes_df)} resumes")
        return resumes_df
    
    def extract_jobs(self, keywords="python developer"):
        """Extract job descriptions"""
        logger.info("Extracting job descriptions...")
        jobs_df = self.job_scraper.scrape_jobs_basic(keywords)
        logger.info(f"Extracted {len(jobs_df)} job descriptions")
        return jobs_df
    
    def transform_resumes(self, resumes_df):
        """Transform resume data"""
        logger.info("Transforming resumes...")
        
        transformed_resumes = []
        for _, resume in tqdm(resumes_df.iterrows(), total=len(resumes_df)):
            # Process text
            processed_content = self.text_processor.preprocess_text(resume['content'])
            
            # Extract skills
            skills = self.text_processor.extract_skills(resume['content'])
            
            transformed_resumes.append({
                'filename': resume['filename'],
                'content': resume['content'],
                'processed_content': processed_content,
                'skills': ', '.join(skills),
                'experience': ''  # Could extract experience years with more advanced NLP
            })
        
        return pd.DataFrame(transformed_resumes)
    
    def transform_jobs(self, jobs_df):
        """Transform job description data"""
        logger.info("Transforming job descriptions...")
        
        transformed_jobs = []
        for _, job in tqdm(jobs_df.iterrows(), total=len(jobs_df)):
            # Process text
            processed_content = self.text_processor.preprocess_text(job['content'])
            
            # Extract required skills
            required_skills = self.text_processor.extract_skills(job['content'])
            
            transformed_jobs.append({
                'title': job['title'],
                'company': job['company'],
                'content': job['content'],
                'processed_content': processed_content,
                'required_skills': ', '.join(required_skills)
            })
        
        return pd.DataFrame(transformed_jobs)
    
    def load_data(self, resumes_df, jobs_df):
        """Load data into database"""
        logger.info("Loading data into database...")
        
        # Load resumes
        for _, resume in resumes_df.iterrows():
            try:
                self.db.insert_resume(
                    filename=resume['filename'],
                    content=resume['content'],
                    processed_content=resume['processed_content'],
                    skills=resume['skills'],
                    experience=resume['experience']
                )
            except Exception as e:
                logger.warning(f"Resume already exists or error: {e}")
        
        # Load jobs
        for _, job in jobs_df.iterrows():
            try:
                self.db.insert_job(
                    title=job['title'],
                    company=job['company'],
                    content=job['content'],
                    processed_content=job['processed_content'],
                    required_skills=job['required_skills']
                )
            except Exception as e:
                logger.warning(f"Job already exists or error: {e}")
    
    def run_etl(self):
        """Run complete ETL pipeline"""
        logger.info("Starting ETL pipeline...")
        
        # Extract
        resumes_df = self.extract_resumes()
        jobs_df = self.extract_jobs()
        
        # Transform
        if not resumes_df.empty:
            resumes_df = self.transform_resumes(resumes_df)
        if not jobs_df.empty:
            jobs_df = self.transform_jobs(jobs_df)
        
        # Load
        self.load_data(resumes_df, jobs_df)
        
        logger.info("ETL pipeline completed successfully!")
        return resumes_df, jobs_df