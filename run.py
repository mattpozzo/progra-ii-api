from app import create_app
from dotenv import load_dotenv
from fin_test import delete_all
from app.utils.muscles import muscles_seeder

delete_all()  # keep while testing
load_dotenv()

app, db = create_app()

if __name__ == '__main__':
    with app.app_context():
        muscles_seeder(db)
    app.run()
