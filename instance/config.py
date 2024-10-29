import os


env = os.environ.get("FLASK_ENV", "Dev")
# db_username = os.environ.get("DB_USERNAME")
# db_password = os.environ.get("DB_PASSWORD")
db_username = "testuser"
db_password = "sW5KMr5xiTWA"


if env == "Dev":
    DATABASE_URI = "mysql+pymysql://testuser:sW5KMr5xiTWA@localhost:3306/blog_app"
    SECRET_KEY = "dev-secret-key"
    DEBUG = True
    
elif env == "Test":
    DATABASE_URI = "sqlite:///blog_app.db"
    SECRET_KEY = "test-secret-key"
    DEBUG = True
    
# elif env == "Prd":
    