import datetime
from . import db
from sqlalchemy import Integer, String, ForeignKey, DateTime, Float, Index

class EnvironmentalData(db.Model):
    id = db.Column(Integer, primary_key=True)
    greenhouse_id = db.Column(Integer, ForeignKey('greenhouse.id'), nullable=False, index=True)
    temperature = db.Column(Float, nullable=False)
    humidity = db.Column(Float, nullable=False)
    co2 = db.Column(Float, nullable=False)
    light_intensity = db.Column(Float, nullable=False)
    soil_ph = db.Column(Float, nullable=False)
    soil_moisture = db.Column(Float, nullable=False)
    timestamp = db.Column(DateTime, default=datetime.datetime.utcnow, index=True)
    source = db.Column(String(20), nullable=False, default='manual', index=True)

    def __repr__(self):
         return f'<EnvData G{self.greenhouse_id} @ {self.timestamp}>'