import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from settings import DB_NAME, DB_USER, DB_PASSWORD, TEST_DB_NAME, TEST_DB_USER, TEST_DB_PASSWORD, SINGER_TOKEN, DIRECTOR_TOKEN





database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, 'localhost:5432', DB_NAME)
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Singer(db.Model):
    __tablename__ = 'singer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    voice_part = db.Column(db.String(), nullable=False)
    not_available = db.Column(db.String(), nullable=False)
    enrollment = db.relationship('ChoirEnrollment', backref='singer', lazy=True)

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'voice_part': self.voice_part
        }

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'voice_part': self.voice_part,
            'not_avilable': self.not_available
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())

class Choir(db.Model):
    __tablename__ = 'choir'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    practice_time = db.Column(db.String(), nullable=True)
    enrollment = db.relationship('ChoirEnrollment', backref='choir', lazy=True)

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'practice time': self.practice_time
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()



    def __repr__(self):

        return json.dumps(self.long())



class ChoirEnrollment(db.Model):
    __tablename__ = 'enrollment'

    id = db.Column(db.Integer, primary_key=True)
    choir_id = db.Column(db.Integer, db.ForeignKey('choir.id'), nullable=False)
    singer_id = db.Column(db.Integer, db.ForeignKey('singer.id'), nullable=False)

    def enroll(self):
        db.session.add(self)
        db.session.commit()

    def unenroll(self):
        db.session.delete(self)
        db.session.commit()