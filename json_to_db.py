import csv
from models import db, Meal, Category

with open('svs-file.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] != 'id':
            print(row)
            meal = Meal(title=row[1], price=row[2], description=row[3], picture=row[4], category_id=row[5])
            db.session.add(meal)
    db.session.commit()
