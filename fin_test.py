from app import create_app
from dotenv import load_dotenv

load_dotenv()

app, db = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()