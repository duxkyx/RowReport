# Vercel connection
import sys
import os

# Add Backend to Python path
sys.path.append(os.path.abspath("Backend"))

from API.main import app  # must be named `app`


