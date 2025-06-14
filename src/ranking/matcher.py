import pandas as pd
from src.utils.database import DatabaseManager
from src.nlp.text_processor import TextProcessor
import logging

logger = logging.getLogger(__name__)

class ResumeJobMatcher:
    def __init__(self):
        self.db = DatabaseManager()
        self.text_processor = TextProcessor()
    
    def calculate_matches(self, top_k=5):
        """Calculate similarity scores between all resumes and jobs"""
        logger.info("Calculating resume-job matches...")
        
        # Get data from database
        resumes_df = self.db.get_resumes()
        jobs_df = self.db.get_jobs()
        
        if resumes_df.empty or jobs_df.empty:
            logger.warning("No resumes or jobs found in database")
            return pd.DataFrame()
        
        matches = []
        
        # Calculate similarities
        for _, resume in resumes_df.iterrows():
            resume_scores = []
            
            for _, job in jobs_df.iterrows():
                # Content similarity
                content_similarity = self.text_processor.calculate_similarity(
                    resume['processed_content'],
                    job['processed_content']
                )
                
                # Skills similarity
                skills_similarity = self._calculate_skills_similarity(
                    resume['skills'],
                    job['required_skills']
                )
                
                # Combined score (weighted)
                combined_score = (0.7 * content_similarity + 0.3 * skills_similarity)
                
                resume_scores.append({
                    'resume_id': resume['id'],
                    'resume_filename': resume['filename'],
                    'job_id': job['id'],
                    'job_title': job['title'],
                    'company': job['company'],
                    'content_similarity': content_similarity,
                    'skills_similarity': skills_similarity,
                    'combined_score': combined_score
                })
            
            # Sort jobs by score for this resume
            resume_scores = sorted(resume_scores, key=lambda x: x['combined_score'], reverse=True)
            
            # Add rank and take top K
            for rank, match in enumerate(resume_scores[:top_k], 1):
                match['rank'] = rank
                matches.append(match)
        
        matches_df = pd.DataFrame(matches)
        
        # Save to database
        self._save_matches(matches_df)
        
        return matches_df
    
    def _calculate_skills_similarity(self, resume_skills, job_skills):
        """Calculate similarity between skill sets"""
        if not resume_skills or not job_skills:
            return 0.0
        
        resume_skills_set = set(skill.strip().lower() for skill in resume_skills.split(',') if skill.strip())
        job_skills_set = set(skill.strip().lower() for skill in job_skills.split(',') if skill.strip())
        
        if not resume_skills_set or not job_skills_set:
            return 0.0
        
        # Jaccard similarity
        intersection = len(resume_skills_set.intersection(job_skills_set))
        union = len(resume_skills_set.union(job_skills_set))
        
        return intersection / union if union > 0 else 0.0
    
    def _save_matches(self, matches_df):
        """Save matches to database"""
        try:
            matches_df.to_sql('matches', self.db.engine, if_exists='replace', index=False)
            logger.info(f"Saved {len(matches_df)} matches to database")
        except Exception as e:
            logger.error(f"Error saving matches: {e}")
    
    def get_top_matches_for_resume(self, resume_filename, top_k=5):
        """Get top job matches for a specific resume"""
        query = f"""
        SELECT m.*, r.filename, j.title, j.company
        FROM matches m
        JOIN resumes r ON m.resume_id = r.id
        JOIN job_descriptions j ON m.job_id = j.id
        WHERE r.filename = '{resume_filename}'
        ORDER BY m.combined_score DESC
        LIMIT {top_k}
        """
        
        return pd.read_sql(query, self.db.engine)
    
    def get_match_summary(self):
        """Get summary of all matches"""
        query = """
        SELECT 
            r.filename as resume,
            j.title as job_title,
            j.company,
            m.combined_score,
            m.rank
        FROM matches m
        JOIN resumes r ON m.resume_id = r.id
        JOIN job_descriptions j ON m.job_id = j.id
        ORDER BY r.filename, m.rank
        """
        
        return pd.read_sql(query, self.db.engine)