from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .greenhouse import Greenhouse
from .issue import Issue
from .employee import Employee
from .enviromental_data import EnvironmentalData
