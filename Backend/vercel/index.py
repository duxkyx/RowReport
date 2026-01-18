# Vercel connection
import sys
import os

sys.path.append(os.path.abspath("API"))
sys.path.append(os.path.abspath("Database"))

from API.main import app  # must be named `app`


