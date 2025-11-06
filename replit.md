# Complaint Management System

## Overview

A full-stack complaint management system with role-based access control. The system provides a complete complaint lifecycle workflow from submission through resolution, with support for categorization, assignment, comments, and status tracking. Built for Python 3.11.9 with a FastAPI REST API backend and Streamlit web interface.

**Current Status**: Fully functional MVP with both backend (port 8000) and frontend (port 5000) workflows running successfully. PostgreSQL database configured and seeded with initial data.

**Recent Changes (November 6, 2025)**:
- Complete backend API implementation with FastAPI + SQLAlchemy 2.x
- Streamlit frontend with user selection, complaint creation, viewing, and commenting
- PostgreSQL database integration with automatic table creation and data seeding
- Workflows configured and running: backend (console, port 8000) and frontend (webview, port 5000)
- Additional packages installed: psycopg2-binary (PostgreSQL driver), email-validator (for Pydantic EmailStr)

**Architect Review Recommendations for Future Enhancement**:
1. Expand CRUD operations: Add UPDATE and DELETE endpoints for users, categories, comments, status history, and attachments
2. Enhanced frontend features: Add attachment upload/display interface and detailed status history view
3. Validation improvements: Add foreign key validation in comment/status/attachment creation to prevent invalid references

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture

**Framework**: FastAPI with async-capable architecture, though currently using synchronous database operations.

**API Design**: RESTful API following versioned endpoint structure (`/api/v1/*`) with resource-based routing:
- `/users` - User management endpoints
- `/categories` - Complaint category management
- `/complaints` - Complaint CRUD operations with nested routes for comments and status updates

**Data Access Pattern**: Repository pattern implemented through `crud.py` module, separating database operations from route handlers. SQLAlchemy 2.x ORM provides the data access layer with declarative models.

**Database Strategy**: Flexible database configuration supporting both MySQL (production) and SQLite (development/testing) through environment-based connection strings. Database connection pooling enabled with `pool_pre_ping=True` for connection health checks.

**Authentication/Authorization**: Currently no authentication mechanism implemented. Role-based access control defined in user model (`admin`/`user` roles) but not enforced at API layer. **Future implementation needed**: JWT tokens or session-based auth to secure endpoints and enforce role permissions.

**Application Lifecycle**: 
- Automatic table creation on startup using SQLAlchemy metadata
- Seed data initialization for default users and categories
- CORS enabled for cross-origin requests (currently allowing all origins)

**Trade-offs**: 
- Simple synchronous database operations chosen over async for development speed, though FastAPI supports async
- No authentication allows rapid prototyping but requires implementation before production use
- Open CORS policy simplifies development but needs restriction in production

### Frontend Architecture

**Framework**: Streamlit for rapid web UI development with minimal JavaScript requirements.

**API Communication**: Direct HTTP requests to FastAPI backend using `requests` library. API base URL configured via environment variables for deployment flexibility.

**State Management**: Streamlit's built-in session state and automatic re-run mechanism. No complex state management library needed due to Streamlit's reactive model.

**UI Components**: Utilizes Streamlit's native widgets for forms, tables, and data display. Wide layout mode enabled for better space utilization.

**Deployment Separation**: Frontend and backend run as separate processes, allowing independent scaling and deployment. Frontend acts as API client rather than server-side rendering.

### Data Model Design

**Core Entities**:
- `User` - System users with role-based access
- `ComplaintCategory` - Organizational categories for complaints
- `Complaint` - Central entity with status workflow (open → in-progress → resolved → closed)
- `ComplaintComment` - Threaded discussion on complaints
- `ComplaintStatusHistory` - Audit trail for status changes
- `ComplaintAttachment` - File attachments (model defined but not fully implemented)

**Relationships**:
- Users create complaints (one-to-many)
- Complaints assigned to users for resolution (optional many-to-one)
- Categories organize complaints (many-to-one)
- Cascade deletes configured for dependent entities (comments, history, attachments)

**Design Decisions**:
- Soft deletion not implemented; uses hard deletes with CASCADE
- Timestamps auto-managed by database (`server_default=func.now()`)
- String-based status field rather than enum for flexibility
- Separate assigned_to field allows complaint reassignment

### Database Layer

**ORM**: SQLAlchemy 2.x with declarative base models. Chosen for:
- Strong typing and IDE support
- Automatic relationship management
- Database abstraction allowing MySQL/SQLite switching

**Connection Management**: 
- Session-per-request pattern using FastAPI dependency injection
- Connection pooling for MySQL with health checks
- SQLite fallback for testing/development with thread-safety configuration

**Migration Strategy**: Currently using `create_all()` for table creation. **Production consideration**: Should implement Alembic migrations for schema versioning and zero-downtime updates.

**Schema Organization**:
- Foreign keys enforce referential integrity
- Indexes on frequently queried fields (email, user_id, category_id)
- Automatic timestamp management for audit trails

## External Dependencies

### Database Systems

**MySQL** (Production):
- Primary database supporting production workloads
- Requires PyMySQL driver for pure-Python connectivity
- Connection string format: `mysql+pymysql://user:password@host:port/database`
- Recommended services: PlanetScale, Railway, or other managed MySQL providers

**SQLite** (Development/Testing):
- Fallback database requiring no external service
- File-based storage in `./db.sqlite3`
- Automatically used when DATABASE_URL not configured

### Python Package Dependencies

**Backend Core**:
- `fastapi==0.104.1` - Web framework
- `uvicorn[standard]==0.24.0` - ASGI server with standard extras
- `sqlalchemy>=2.0.23` - ORM framework
- `pymysql==1.1.0` - MySQL database driver
- `cryptography==41.0.7` - Required by PyMySQL for secure connections
- `pydantic>=2.5.0` - Data validation and serialization
- `python-dotenv==1.0.0` - Environment variable management

**Frontend Core**:
- `streamlit==1.28.2` - Web UI framework
- `requests==2.31.0` - HTTP client for API calls
- `python-dotenv==1.0.0` - Environment configuration
- `pandas==2.1.3` - Data manipulation (for Streamlit tables)

### Environment Configuration

**Required Variables**:
- `DATABASE_URL` - Database connection string (defaults to SQLite if not set)
- `API_BASE_URL` - Backend API endpoint for frontend (defaults to `http://localhost:8000`)

**Configuration Sources**:
- `.env` file for local development
- Replit Secrets for cloud deployment
- Environment variables for container deployments

### Third-Party Services

**None currently integrated**, but architecture supports:
- Email services for notifications (SMTP integration point needed)
- File storage services for attachments (S3, Cloudinary, etc.)
- Authentication providers (OAuth, Auth0, etc.)