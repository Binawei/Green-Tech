
from . import db

from sqlalchemy import Integer, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

employee_greenhouse_association = Table('employee_greenhouse_association', db.metadata,
    db.Column('employee_id', Integer, ForeignKey('employee.id'), primary_key=True),
    db.Column('greenhouse_id', Integer, ForeignKey('greenhouse.id'), primary_key=True),
    db.Index('ix_employee_greenhouse_employee_id', 'employee_id'),
    db.Index('ix_employee_greenhouse_greenhouse_id', 'greenhouse_id')
)

class Employee(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    email = db.Column(String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(String(256), nullable=False)
    phone_number = db.Column(String(20), nullable=True)
    available = db.Column(Boolean, nullable=False, default=True)
    company_id = db.Column(String(10), unique=True, nullable=False)
    is_admin = db.Column(Boolean, default=False, nullable=False)

    # --- Many-to-Many Relationship to Greenhouse ---
    greenhouses = relationship(
        'Greenhouse',
        secondary=employee_greenhouse_association,
        lazy='select',
        back_populates='employees'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        num_greenhouses = len(self.greenhouses) if self.greenhouses else 0
        return f'<Employee {self.id}: {self.name} ({self.email}) - {num_greenhouses} GH>'