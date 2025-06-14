import pandas as pd
import time


class JobScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def create_sample_jobs(self):
        """Create sample job descriptions for testing"""
        sample_jobs = [
            {
                'title': 'Python Developer',
                'company': 'Tech Corp',
                'content': '''We are looking for a Python Developer with experience in:
                - Python programming (3+ years)
                - Django/Flask frameworks
                - REST API development
                - Database design (PostgreSQL, MySQL)
                - Git version control
                - Agile development methodologies
                
                Responsibilities:
                - Develop web applications using Python
                - Design and implement APIs
                - Work with databases
                - Collaborate with cross-functional teams
                
                Requirements:
                - Bachelor's degree in Computer Science
                - Strong problem-solving skills
                - Experience with cloud platforms (AWS, Azure)
                '''
            },
            {
                'title': 'Data Scientist',
                'company': 'Data Analytics Inc',
                'content': '''Looking for a Data Scientist to join our team:
                
                Required Skills:
                - Python/R programming
                - Machine Learning (scikit-learn, TensorFlow)
                - Data visualization (matplotlib, seaborn, plotly)
                - SQL and database management
                - Statistical analysis
                - Pandas, NumPy
                
                Responsibilities:
                - Build predictive models
                - Analyze large datasets
                - Create data visualizations
                - Present findings to stakeholders
                
                Preferred:
                - PhD in Statistics, Math, or related field
                - Experience with big data tools (Spark, Hadoop)
                - Cloud platforms experience
                '''
            },
            {
                'title': 'Full Stack Developer',
                'company': 'Startup XYZ',
                'content': '''Full Stack Developer position available:
                
                Technical Requirements:
                - JavaScript (ES6+)
                - React.js or Vue.js
                - Node.js
                - Express.js
                - MongoDB or PostgreSQL
                - HTML5/CSS3
                - Git version control
                
                Nice to have:
                - Python or Java backend experience
                - Docker containerization
                - AWS/GCP experience
                - GraphQL
                - TypeScript
                
                You will:
                - Develop both frontend and backend components
                - Design responsive web applications
                - Optimize application performance
                - Participate in code reviews
                '''
            }
        ]
        
        return pd.DataFrame(sample_jobs)
    
    def scrape_jobs_basic(self, keywords="python developer", num_jobs=10):
        """Basic job scraping simulation"""
        # For demo purposes, return sample data
        # In production, implement actual scraping with proper rate limiting
        print(f"Simulating scraping for '{keywords}'...")
        time.sleep(2)  # Simulate API delay
        
        return self.create_sample_jobs()