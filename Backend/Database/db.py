from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os

# Load .env automatically
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

DB_USER = os.getenv("DB_USER").strip()
DB_PASSWORD = os.getenv("DB_PASSWORD").strip()
DB_HOST = os.getenv("DB_HOST").strip()
DB_PORT = os.getenv("DB_PORT", "5432").strip()
DB_NAME = os.getenv("DB_NAME").strip()
DB_PGSSLMODE = os.getenv('DB_PGSSLMODE', "require").strip()
DB_PGCHANNELBINDING = os.getenv('DB_PGCHANNELBINDING', "require").strip()

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?sslmode={DB_PGSSLMODE}&channel_binding={DB_PGCHANNELBINDING}"
)
print("DATABASE_URL =", DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session