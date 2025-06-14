# API Documentation

## Core Classes

### TextProcessor
Handles all NLP operations including text cleaning, skill extraction, and similarity calculations.

```python
from src.nlp.text_processor import TextProcessor

processor = TextProcessor()

# Clean text
cleaned = processor.clean_text("Raw text with symbols!")

# Extract skills
skills = processor.extract_skills("Python, JavaScript, SQL experience")

# Calculate similarity
similarity = processor.calculate_similarity(text1, text2)