# HolaBox Backend Project

## Overview
HolaBox is a production-grade cloud storage backend API built with Python and FastAPI. It provides complete file management, user authentication, sharing capabilities, and premium subscription features similar to TeraBox.

## Current State
- ✅ Fully functional FastAPI backend running on port 5000
- ✅ Complete authentication system with JWT tokens
- ✅ File upload/download with folder management
- ✅ Soft delete and trash system
- ✅ Public sharing with password protection and expiry
- ✅ Premium subscription system (Free, Premium, Ultra plans)
- ✅ Admin panel for user and storage management
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Storage quota enforcement

## Recent Changes
- **2025-11-17**: Initial project creation with complete backend implementation
  - Created all database models (User, File, Folder, Share, Subscription)
  - Implemented JWT authentication with access and refresh tokens
  - Built file storage engine with local filesystem organization
  - Added sharing system with public links and access control
  - Created premium subscription management
  - Implemented admin endpoints for user management
  - Configured workflow to run uvicorn server on port 5000

## Project Architecture

### Technology Stack
- **Framework**: FastAPI (async Python web framework)
- **Database**: SQLAlchemy ORM with SQLite (upgradeable to PostgreSQL)
- **Authentication**: JWT tokens with python-jose and bcrypt password hashing
- **File Handling**: aiofiles for async file operations
- **Validation**: Pydantic v2 for request/response validation

### Key Components
1. **Authentication** (`app/auth/`): JWT-based auth with register, login, refresh, password change
2. **Users** (`app/users/`): User profile management and storage quota tracking
3. **Storage** (`app/storage/`): File upload/download, folder management, soft delete
4. **Sharing** (`app/sharing/`): Public link generation with password protection and expiry
5. **Premium** (`app/premium/`): Subscription management and plan upgrades
6. **Admin** (`app/admin/`): User management, storage monitoring, server statistics

### Storage System
- Files stored in `/storage/{userId}/` directory structure
- Metadata tracked in database (File and Folder models)
- Storage quotas: Free (20GB), Premium (1TB), Ultra (2TB)
- Automatic storage calculation and enforcement

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get tokens
- `POST /auth/refresh` - Refresh access token
- `POST /auth/change-password` - Change password
- `POST /auth/logout` - Logout

### Users
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update profile
- `GET /users/storage` - Get storage usage info

### Storage
- `POST /storage/folders` - Create folder
- `GET /storage/folders` - List folders
- `POST /storage/upload` - Upload file
- `GET /storage/files` - List files
- `GET /storage/files/{id}/download` - Download file
- `DELETE /storage/files/{id}` - Move to trash
- `POST /storage/files/{id}/restore` - Restore from trash
- `PUT /storage/files/{id}/rename` - Rename file

### Sharing
- `POST /shares/` - Create share link
- `GET /shares/my-shares` - List user's shares
- `GET /shares/{token}/access` - Access shared file
- `GET /shares/{token}/download` - Download shared file
- `DELETE /shares/{id}` - Delete share

### Premium
- `GET /premium/plans` - Available plans
- `POST /premium/upgrade` - Upgrade plan
- `GET /premium/subscription` - Current subscription

### Admin
- `GET /admin/users` - List all users
- `POST /admin/users/{id}/suspend` - Suspend user
- `POST /admin/users/{id}/activate` - Activate user
- `POST /admin/users/{id}/reset-storage` - Recalculate storage
- `GET /admin/stats` - Server statistics

## Running the Project

The server is configured to run automatically via workflow:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

Access the API:
- API Root: `http://localhost:5000/`
- Interactive Docs: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`

## Environment Variables

Located in `.env`:
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT signing key
- `ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiry (30 min)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiry (7 days)
- `STORAGE_PATH`: File storage directory (./storage)

## Database Models

### User
- Authentication and profile data
- Plan type and storage usage
- Last login and upload tracking

### File
- File metadata (name, size, MIME type)
- Storage path reference
- View/download counts
- Soft delete support

### Folder
- Hierarchical folder structure
- User-based organization
- Soft delete support

### Share
- Public share tokens
- Password protection (optional)
- Expiry dates (optional)
- Access tracking

### Subscription
- Plan type (free, premium, ultra)
- Payment tracking
- Active status and dates

## Security Features
- Bcrypt password hashing
- JWT access and refresh tokens
- User-based file access control
- Password-protected shares
- Admin-only endpoints
- CORS middleware configured

## Future Enhancements
- Email verification system
- Forgot password with email reset
- Redis caching for metadata
- MinIO/S3 integration for scalable storage
- Resume upload support (chunked uploads)
- Image thumbnail generation
- Video streaming optimization
- Automated trash cleanup (30-day deletion)
- Comprehensive test suite
- Rate limiting
- Audit logs

## User Preferences
- Default database: SQLite (easily upgradeable to PostgreSQL)
- File storage: Local filesystem (upgradeable to object storage)
- Authentication: JWT tokens
- API documentation: Swagger UI and ReDoc

## Notes
- Server runs on port 5000 (required for Replit webview)
- Database auto-initializes on startup
- Storage directory created automatically
- All passwords hashed with bcrypt
- File uploads use async operations for performance
- Soft delete allows trash/restore functionality
