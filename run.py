from dotenv import load_dotenv
from app import create_app
import os

load_dotenv()

app = create_app()

if __name__ == '__main__':
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=5000)
    