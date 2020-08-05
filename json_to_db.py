import csv

from models import db, Meal, Category


def csv_to_db():
    with open('svs-file.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != 'id':
                meal = Meal(title=row[1], price=row[2], description=row[3], picture=row[4], category_id=row[5])
                db.session.add(meal)
    with open('delivery_categories.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] != 'title':
                cat = Category(title=row[1])
                db.session.add(cat)
    db.session.commit()


if __name__ == '__main__':
    from app import app

    with app.app_context():
        csv_to_db()
