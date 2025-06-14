#!/usr/bin/env python3
"""Setup script for the resume-job matcher project"""

import subprocess
import sys
import os

def run_command(command):
    """Run a shell command"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {command}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"✗ {command}")
        print(f"Error: {e.stderr}")
        return
def install_requirements():
    """Install Python requirements"""
    print("Installing Python requirements...")
    run_command("pip install -r requirements.txt")

def download_models():
    """Download required NLP models"""
    print("Downloading NLP models...")
    run_command("python -m spacy download en_core_web_sm")
    run_command("python -c \"from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')\"")

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = [
        "data/resumes",
        "data/job_descriptions", 
        "logs",
        "outputs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created {directory}")

def create_sample_data():
    """Create sample resume and job data"""
    print("Creating sample data...")
    
    # Sample resume
    sample_resume = """
John Doe
Software Developer

EXPERIENCE:
- 3 years Python development
- Django and Flask frameworks
- REST API development
- PostgreSQL and MySQL databases
- Git version control
- Agile methodologies

SKILLS:
- Python, JavaScript, SQL
- Django, Flask, React
- PostgreSQL, MySQL, MongoDB
- AWS, Docker
- Machine Learning basics

EDUCATION:
Bachelor of Science in Computer Science
"""
    
    with open("data/resumes/john_doe_resume.txt", "w") as f:
        f.write(sample_resume)
    
    print("✓ Created sample resume")

def main():
    """Main setup function"""
    print("Setting up Resume-Job Matcher project...")
    print("=" * 50)
    
    create_directories()
    install_requirements()
    download_models()
    create_sample_data()
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Add your resumes to data/resumes/")
    print("2. Run: python src/main.py run-etl")
    print("3. Run: python src/main.py calculate-matches")
    print("4. Run: python src/main.py summary")

if __name__ == "__main__":
    main()