# serices/users/project/api/models.py
from sqlalchemy.sql import func
from project import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def to_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active
        }


class Persona(db.Model):
    __tablename__ = 'personas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Float(2), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    smartphones = db.relationship('Smartphone')
    creation_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    modification_date = db.Column(db.DateTime,
                                  default=func.now(),
                                  nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, name, lastname, age, gender):
        self.name = name
        self.lastname = lastname
        self.age = age
        self.gender = gender

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname,
            'age': self.age,
            'gender': self.gender,
            'active': self.active
        }


class Smartphone(db.Model):
    __tablename__ = 'smartphones'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    brand = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float(4), nullable=False)
    color = db.Column(db.String(128), nullable=False)
    quantity = db.Column(db.Float(2), nullable=False)
    propietario = db.Column(db.Integer, db.ForeignKey('personas.id'))
    creation_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    modification_date = db.Column(db.DateTime,
                                  default=func.now(),
                                  nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, **kwargs):
        super(Smartphone, self).__init__(**kwargs)
        # do custom initialization here

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'color': self.color,
            'propietario': self.propietario,
            'quantity': self.quantity,
            'active': self.active
        }
