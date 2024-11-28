import pandas as pd


def exercises_rows() -> list[dict]:
    muscles = pd.read_csv("app/utils/exercises.csv")

    return muscles.to_dict('records')


def exercises_seeder(db):
    from app.models.models import Exercise
    rows = exercises_rows()
    for row in rows:
        muscle = 0
        muscle = Exercise(**row)
        db.session.add(muscle)
    db.session.commit()


if __name__ == '__main__':
    print(exercises_rows())
