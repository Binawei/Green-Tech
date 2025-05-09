# GreenTech: Comprehensive Greenhouse Monitoring and Management System

GreenTech is a web-based application that enables real-time monitoring and management of greenhouse environments, employee assignments, and issue tracking. The system helps greenhouse operators maintain optimal growing conditions by tracking environmental data and alerting staff to potential problems.

The application provides centralized management of multiple greenhouses, with features for monitoring environmental conditions (temperature, humidity, CO2, light intensity, soil pH, and moisture), assigning employees to specific facilities, and tracking/resolving environmental issues. It includes role-based access control with admin and regular user permissions to ensure proper data access and system management.

## Repository Structure
```
.
├── app.py                 # Main Flask application entry point with core routes and logic
├── config.py             # Configuration settings for different environments
├── models/              # Database models and schemas
│   ├── employee.py      # Employee model for user management
│   ├── greenhouse.py    # Greenhouse facility model
│   ├── enviromental_data.py  # Environmental readings model
│   └── issue.py         # Issue tracking model
├── static/             # Static assets
│   └── styles.css      # Application styling
├── templates/          # Jinja2 HTML templates
│   ├── base.html       # Base template with common layout
│   ├── dashboard.html  # Main dashboard view
│   └── various .html   # Other view templates
├── tests/             # Test suite
│   ├── conftest.py    # Test configurations and fixtures
│   └── test_*.py      # Various test modules
├── utils.py           # Utility functions for environmental checks
└── requirements.txt   # Python package dependencies
```

## Usage Instructions
### Prerequisites
- Python 3.12 or higher
- PostgreSQL database (for production)
- SMTP server access (for email notifications)
- Required Python packages listed in requirements.txt

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd greentech

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize the database
flask db upgrade
flask init-db
flask create-admin  # Creates initial admin user
```

### Quick Start
1. Start the development server:
```bash
flask run
```

2. Access the application at http://localhost:5000

3. Log in with the admin credentials:
```
Email: greentechAdmin@gmail.com
Password: (set during create-admin)
```

### More Detailed Examples
1. Adding a New Greenhouse:
```python
# Via Admin Interface
1. Navigate to Greenhouses
2. Click "Add New Greenhouse"
3. Enter name and location
4. Submit form
```

2. Monitoring Environmental Data:
```python
# View current readings
1. Go to Dashboard
2. Click on greenhouse name
3. View real-time environmental data
```

### Troubleshooting
Common Issues:
1. Database Connection Errors
   - Check DATABASE_URL in .env
   - Verify PostgreSQL is running
   - Run `flask db upgrade`

2. Email Notifications Not Working
   - Verify MAIL_* settings in .env
   - Check SMTP server connectivity
   - Enable debug logging: `LOGGING_LEVEL=DEBUG`

3. Access Permission Issues
   - Verify user role assignments
   - Check greenhouse assignments
   - Clear browser session and re-login

## Data Flow
The system processes environmental data from greenhouses and manages user interactions through a multi-tier architecture.

```ascii
[Sensors] -> [Environmental Data] -> [Database]
                     |
                     v
[Users] -> [Web Interface] -> [Business Logic] -> [Issue Detection]
                                    |
                                    v
                           [Email Notifications]
```

Key Component Interactions:
- Environmental data is collected and stored in the database
- Business logic processes readings against thresholds
- Issues are created when thresholds are exceeded
- Notifications are sent to assigned employees
- Users can view and manage data through web interface
- Admin users have additional management capabilities
- Authentication controls access to protected resources