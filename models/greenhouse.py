from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String

class Greenhouse(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    location = db.Column(String(100), nullable=False)
    issue_description = db.Column(String(255), nullable=True)
    status = db.Column(String(255), nullable=True)
    employees = relationship('Employee', backref='assigned_greenhouse', lazy='select')
    environmental_data = relationship('EnvironmentalData', backref='greenhouse', lazy='dynamic') # Use dynamic if you expect many data points
    issues = relationship('Issue', backref='originating_greenhouse', lazy='select', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Greenhouse {self.id}: {self.name}>'