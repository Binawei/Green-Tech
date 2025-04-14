from . import db
from sqlalchemy import Integer, String, ForeignKey, Boolean
from werkzeug.security import generate_password_hash, check_password_hash

class Employee(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    email = db.Column(String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(String(256), nullable=False)
    phone_number = db.Column(String(20), nullable=True)
    available = db.Column(Boolean, nullable=False, default=True)
    greenhouse_id = db.Column(Integer, ForeignKey('greenhouse.id'), nullable=True)
    company_id = db.Column(String(10), unique=True, nullable=False)
    is_admin = db.Column(Boolean, default=False, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Employee {self.id}: {self.name} ({self.email})>'