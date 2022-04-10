from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    # the columns for the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # Store ID in StoreModel
    store = db.relationship('StoreModel') # Find the store in database that match with store_id

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name = ?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()

        # if row:
        #     return cls(*row)  # {'item': { 'name': row[0], 'price': row[1] }}
        return cls.query.filter_by(name=name).first()  # SELECT * FROM __tablename__ WHERE name = name LIMIT 1

    ''' Using SQLAlchemy insert and update do the same thing so will we rename the method to save_to_db'''
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
