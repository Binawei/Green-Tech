import datetime
from . import db
from sqlalchemy import Integer, String, ForeignKey, DateTime, Index

class Issue(db.Model):
    id = db.Column(Integer, primary_key=True)
    greenhouse_id = db.Column(Integer, ForeignKey('greenhouse.id'), nullable=False)
    description = db.Column(String(500), nullable=False)
    status = db.Column(String(20), nullable=False, default='Ongoing', index=True)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow, index=True)
    resolved_at = db.Column(DateTime, nullable=True)

    def __repr__(self):
        return f'<Issue {self.id} - {self.status} for GH {self.greenhouse_id}>'