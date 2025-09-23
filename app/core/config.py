from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv(str("DATABASE_URL"))
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("Algorithm")
EXPIRE_MINUTES = os.getenv("EXPIRE_MINUTES")


