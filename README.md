# ERP POC Manager

A Django web application for managing project teams, tracking daily performance, and monitoring progress for an Apache OFBiz ERP proof of concept project.

## Features

- **User Authentication**: Role-based access (Lead/Member) with registration and login
- **Team Selection**: Candidate evaluation system with scoring (Java, SQL, Team Fit)
- **Project Management**: Task creation, assignment, and tracking with status updates
- **Daily Performance Tracking**: Daily standup logs with yesterday/today/blockers format
- **Meeting Management**: Schedule and track daily standups and weekly reviews
- **Dashboard**: Visual overview with charts, statistics, and recent activities
- **REST API**: RESTful endpoints for tasks and logs
- **Admin Panel**: Comprehensive admin interface for all models
- **External Integration**: Links to GitLab, OpenProject, and custom monitoring tools

## Tech Stack

- **Backend**: Django 4.2.7, Django REST Framework
- **Frontend**: Bootstrap 5.1.3, Chart.js for visualizations
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Additional**: Python monitoring scripts, Excel/PDF reporting

## Quick Start

### Prerequisites

- Python 3.8+
- pip
- Virtual environment tool (venv, virtualenv, or conda)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd erp_poc_manager
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Load sample data (optional)**
   ```bash
   python manage.py loaddata fixtures/users.json
   python manage.py loaddata fixtures/projects.json
   python manage.py loaddata fixtures/candidates.json
   python manage.py loaddata fixtures/tasks.json
   python manage.py loaddata fixtures/daily_logs.json
   python manage.py loaddata fixtures/meetings.json
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - API endpoints: http://127.0.0.1:8000/api/

## Project Structure

```
erp_poc_manager/
├── manage.py
├── requirements.txt
├── fixtures/                 # Sample data
├── static/                   # CSS, JavaScript files
├── templates/                # HTML templates
├── erp_poc_manager/         # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                    # Core app (projects, candidates)
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── auth/                    # Custom user authentication
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── admin.py
├── tasks/                   # Task management
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── api_views.py
│   └── admin.py
├── logs/                    # Daily performance logs
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── api_views.py
└── meetings/                # Meeting scheduling
    ├── models.py
    ├── views.py
    └── admin.py
```

## Key Models

### User (Custom)
- Extends Django's built-in User model
- Roles: Lead (admin) or Member
- Used for authentication and task assignment

### Project
- Project details (name, dates, scope)
- Links to tasks and timeline

### Candidate
- Team selection with scoring system
- Java, SQL, and Team Fit scores
- Automatic total score calculation

### Task
- Task management with assignments
- Status tracking (To Do, In Progress, Done)
- Week-based organization
- Dependencies and duration tracking

### DailyLog
- Daily standup format (yesterday/today/blockers)
- User-specific logs with timestamps
- Comments section for lead feedback

### Meeting
- Daily standups and weekly reviews
- Scheduling and notes management

## API Endpoints

### Tasks API
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get specific task
- `PATCH /api/tasks/{id}/` - Update task
- `GET /api/tasks/stats/` - Get task statistics

### Logs API
- `GET /api/logs/` - List all logs
- `POST /api/logs/` - Create new log
- `GET /api/logs/recent/` - Get recent logs for dashboard
- `GET /api/logs/my_logs/` - Get current user's logs

## Usage Guide

### For Project Leads

1. **Setup**: Create projects and add team members
2. **Team Selection**: Add candidates and use scoring system to select top 4
3. **Task Management**: Create and assign tasks with dependencies
4. **Monitoring**: Review daily logs and provide feedback
5. **Meetings**: Schedule standups and reviews
6. **Reports**: Use admin panel to export data and generate reports

### For Team Members

1. **Daily Logs**: Submit daily updates (yesterday/today/blockers)
2. **Task Updates**: Update task status as work progresses
3. **Meetings**: Participate in scheduled standups and reviews

## External Tool Integration

### GitLab Integration
- Link to project repositories
- Track commit activity (via monitoring script)

### OpenProject Integration
- External project management tool
- Complementary project tracking

### Custom Monitoring
- Python script for Git analysis
- Performance metrics collection
- Automated reporting

## Development

### Adding New Features

1. **Models**: Add to appropriate app's `models.py`
2. **Admin**: Register in `admin.py` for admin interface
3. **Views**: Create views in `views.py`
4. **Templates**: Add HTML templates in `templates/`
5. **URLs**: Update `urls.py` routing
6. **API**: Add serializers and API views if needed

### Database Changes

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files (Production)

```bash
python manage.py collectstatic
```

## Deployment

### Environment Variables

Create a `.env` file for production:

```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgres://user:pass@localhost/dbname
```

### Production Setup

1. **Use PostgreSQL**: Update `DATABASES` in settings.py
2. **Configure Static Files**: Set up WhiteNoise or serve via web server
3. **Use Gunicorn**: Deploy with `gunicorn erp_poc_manager.wsgi:application`
4. **Environment Variables**: Use python-decouple for configuration
5. **Security**: Update `SECRET_KEY`, `ALLOWED_HOSTS`, disable `DEBUG`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Submit a pull request

## Timeline & Milestones

**Week 1**: Environment setup, user authentication, testing framework
**Week 2**: Inventory management, order processing modules
**Week 3**: UI improvements, basic reporting
**Week 4**: Integration testing, final deployment

## Support

For issues and questions:
- Check the Django documentation
- Review model relationships in admin panel
- Use the built-in error pages for debugging
- Monitor logs for API endpoint issues

## License

This project is developed for the Apache OFBiz ERP POC and is intended for internal use.