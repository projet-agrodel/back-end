from dotenv import load_dotenv
from app import create_app
import os

load_dotenv()

os.environ["DATABASE_URL"] = "sqlite:///db-teste.db"

app = create_app()

if __name__ == '__main__':
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug)
    