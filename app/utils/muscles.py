import pandas as pd


def muscles_rows() -> list[dict]:
    muscles = pd.read_csv("app/utils/muscles.csv")

    return muscles.to_dict('records')


def muscles_seeder(db):
    from app.models.models import Muscle

    if Muscle.query.first() is None:
        # tabla vacía, le cargamos los datos
        rows = muscles_rows()
        for row in rows:
            muscle = 0
            muscle = Muscle(**row)
            db.session.add(muscle)
        db.session.commit()


if __name__ == '__main__':
    print(muscles_rows())
