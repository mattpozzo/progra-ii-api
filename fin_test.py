from app import create_app
from dotenv import load_dotenv

load_dotenv()

app, db = create_app()


def delete_all():
    with app.app_context():
        db.drop_all()


if __name__ == '__main__':
    delete_all()
