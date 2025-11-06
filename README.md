# Complaint Management System

A full-stack complaint management system built with FastAPI backend and Streamlit frontend, optimized for Python 3.11.9 with MySQL/SQLite support.

## Features

- **User Management**: Create and manage users with role-based access (admin/user)
- **Category Management**: Organize complaints into categories
- **Complaint Tracking**: Full complaint lifecycle management (open, in-progress, resolved, closed)
- **Comments System**: Add comments and updates to complaints
- **Status History**: Track all status changes with timestamps and remarks
- **Admin Panel**: Update status, assign complaints, and manage the system
- **Database Flexibility**: Supports both MySQL (production) and SQLite (testing)

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy 2.x + Pydantic v2
- **Frontend**: Streamlit
- **Database**: MySQL (primary), SQLite (fallback)
- **ORM Driver**: PyMySQL
- **Python**: 3.11.9

## Project Structure

```
complaint-system/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app with startup logic
│   │   ├── database.py          # Database connection
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── crud.py              # CRUD operations
│   │   └── routers/             # API route handlers
│   │       ├── users.py
│   │       ├── categories.py
│   │       └── complaints.py
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py         # Streamlit UI
│   └── requirements.txt
├── db_init/
│   ├── create_tables.sql        # Reference SQL schema
│   └── seed_dummy_data.sql      # Reference seed data
├── .env.example                 # Environment variables template
├── .gitignore
└── README.md
```

## Quick Start

### 1. Environment Setup

Create a `.env` file in the root directory:

```bash
# For SQLite (local testing - default)
DATABASE_URL=sqlite:///./db.sqlite3

# For MySQL (production - PlanetScale, Railway, etc.)
# DATABASE_URL=mysql+pymysql://username:password@hostname:3306/complaint_db

# Backend API URL
API_BASE_URL=http://localhost:8000
```

### 2. Install Dependencies

Dependencies are already installed in this Replit environment.

### 3. Run the Application

The system has two workflows configured:

1. **Backend API** (runs on port 8000)
2. **Frontend UI** (runs on port 5000)

Both will start automatically when you run the project.

### 4. Access the Application

- **Backend API Docs**: http://localhost:8000/docs
- **Frontend UI**: http://localhost:5000
- **Health Check**: http://localhost:8000/health

## Database

### Automatic Initialization

The database tables and seed data are automatically created when the backend starts for the first time.

### Manual Initialization

To manually initialize the database:

```bash
python backend/app/main.py --init-db
```

### Seed Data

The system creates the following default data:
- **Users**: Admin User, John Doe, Jane Smith, Support Team
- **Categories**: Technical, Billing, Service, General
- **Sample Complaints**: 2 demo complaints

## API Endpoints

### Users
- `POST /api/v1/users` - Create a user
- `GET /api/v1/users` - List all users
- `GET /api/v1/users/{user_id}` - Get user by ID

### Categories
- `POST /api/v1/categories` - Create a category
- `GET /api/v1/categories` - List all categories
- `GET /api/v1/categories/{category_id}` - Get category by ID

### Complaints
- `POST /api/v1/complaints` - Create a complaint
- `GET /api/v1/complaints` - List complaints (with filters)
- `GET /api/v1/complaints/{complaint_id}` - Get complaint by ID
- `PATCH /api/v1/complaints/{complaint_id}` - Update complaint
- `POST /api/v1/complaints/{complaint_id}/comments` - Add comment
- `GET /api/v1/complaints/{complaint_id}/comments` - Get comments
- `POST /api/v1/complaints/{complaint_id}/status` - Update status
- `GET /api/v1/complaints/{complaint_id}/status-history` - Get status history
- `POST /api/v1/complaints/{complaint_id}/attachments` - Add attachment metadata
- `GET /api/v1/complaints/{complaint_id}/attachments` - Get attachments

## Using the Frontend

### User Selection
Select a user from the sidebar dropdown to simulate different users (admin/regular user).

### Creating Complaints
1. Select "Create Complaint" from the menu
2. Fill in the title, category, and description
3. Click "Submit Complaint"

### Viewing Complaints
1. Select "View Complaints" from the menu
2. Filter by status and category
3. Expand any complaint to see details
4. Add comments and update status (admin only)

### My Complaints
1. Select "My Complaints" to see only your submitted complaints
2. Add comments to track progress

## Production Deployment

### Using MySQL (Recommended)

1. Create a MySQL database on:
   - [PlanetScale](https://planetscale.com/)
   - [Railway](https://railway.app/)
   - Any MySQL hosting provider

2. Update `.env` or Replit Secrets:
   ```
   DATABASE_URL=mysql+pymysql://user:pass@host:3306/dbname
   ```

3. The application will automatically create tables on first run

### Important Notes for Replit

- Use external MySQL to persist data across restarts
- SQLite data may be lost when the container restarts
- Store `DATABASE_URL` in Replit Secrets for security
- Don't use "Always On" on free plan to conserve credits

## Testing with cURL

```bash
# Create a user
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test User","email":"test@example.com","role":"user"}'

# Create a complaint
curl -X POST http://localhost:8000/api/v1/complaints \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"category_id":1,"title":"Test Issue","description":"Test description"}'

# List all complaints
curl http://localhost:8000/api/v1/complaints

# Filter complaints by status
curl "http://localhost:8000/api/v1/complaints?status=open"
```

## Development

### Database Models

The system includes six main tables:
- `users`: User accounts with roles
- `complaint_categories`: Complaint categorization
- `complaints`: Main complaint records
- `complaint_comments`: User comments on complaints
- `complaint_status_history`: Status change tracking
- `complaint_attachments`: File attachment metadata

### Status Values
- `open`: Newly created complaint
- `in_progress`: Being worked on
- `resolved`: Solution provided
- `closed`: Completed and closed

## Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify DATABASE_URL is set correctly
- Check backend logs for errors

### Frontend can't connect
- Ensure backend is running on port 8000
- Check API_BASE_URL in .env
- Verify network connectivity

### Database errors
- For SQLite: Check file permissions
- For MySQL: Verify connection string and credentials
- Check if database exists and is accessible

## License

This project is optimized for educational and development purposes.
