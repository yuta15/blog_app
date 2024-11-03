from dotenv import load_dotenv
import os

load_dotenv()

env = os.environ.get("ENV", "Dev")
db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_port = os.environ.get("DB_PORT")

secret_key = os.environ.get("SECRET_KEY")


if env == "Test":
    DATABASE_URI = f"sqlite://{db_username}:{db_password}@localhost:{db_port}/blog_app"
    SECRET_KEY = secret_key
    DEBUG = True
    UPLOAD_FOLDER = os.path.join(os.curdir, "blog_content")
    ALLOWED_EXTENSIONS = {'.md'}
    ROOT_PATH = os.curdir
    DEBUG = True
    TESTING = True
