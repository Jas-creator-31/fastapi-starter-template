import os 
from dotenv import load_dotenv

load_dotenv()

self_url = os.getenv("SELF_URL", "")

db_driver_name = "postgresql+asyncpg" # default
db_username = os.getenv("DB_USERNAME", "")
db_secret_key = os.getenv("DB_SECRET_KEY", "")
db_host = os.getenv("DB_HOST", "")
db_port = int(os.getenv("DB_PORT", ""))
db_name = os.getenv("DB_NAME", "")

redis_host = os.getenv("REDIS_HOST", "")
redis_port = int(os.getenv("REDIS_PORT", ""))
redis_db = int(os.getenv("REDIS_DB", ""))

jwt_algorithm = "<JwtAlgorithm>"
jwt_secret = os.getenv("JWT_SECRET_KEY", "")

csrf_key = os.getenv("CSRF_SECRET_KEY", "")
