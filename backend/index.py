# Vercel connection
import sys
import os

sys.path.append(os.path.abspath("api_directory"))
sys.path.append(os.path.abspath("database_directory"))

from api_directory.main import app  # must be named `app`


