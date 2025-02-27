import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Analysis Settings
MAX_LINE_LENGTH = 100
MIN_COMMENT_RATIO = 0.1
COMPLEXITY_THRESHOLD = 10

# Supported file extensions
SUPPORTED_EXTENSIONS = {'.py', '.js', '.java', '.cpp', '.ts'}