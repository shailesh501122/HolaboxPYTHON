# HolaBox - Cloud Storage API

A production-grade cloud storage backend built with Python and FastAPI, similar to TeraBox. This backend provides complete file management, user authentication, sharing capabilities, and premium subscription features.

## 🚀 Features

### 1. User Authentication (JWT)
- User registration and login
- JWT access and refresh tokens
- Password change functionality
- Account settings management
- Session-based authentication

### 2. Cloud Storage
- **File Upload**: Upload files of any size with multipart support
- **File Management**: Download, rename, move, and delete files
- **Folder System**: Create and manage folder hierarchies
- **Soft Delete**: Trash system with restore functionality
- **File Metadata**: Track file size, MIME type, view/download counts

### 3. File Storage System
- Files organized by user ID: `/storage/{userId}/`
- Metadata stored in database
- Storage quota enforcement based on user plan
- Automatic storage calculation

### 4. Sharing System
- Generate public share links
- Optional password protection
- Expiry options (24h, 7d, 30d, or custom)
- Track view and download counts
- Deactivate/delete shares

### 5. Premium Subscriptions
**Plans:**
- **Free**: 20 GB storage
- **Premium**: 1 TB storage - $9.99/month
- **Ultra**: 2 TB storage - $19.99/month

**Features:**
- Plan upgrades
- Payment simulation API
- Storage limit enforcement

### 6. Analytics
- Last login tracking
- Total upload counts
- File view and download statistics
- Storage usage monitoring

### 7. Admin Panel
- Manage all users
- Suspend/activate user accounts
- Reset storage calculations
- View server statistics
- Monitor system usage

## 📦 Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: SQLite (default) / PostgreSQL (production)
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt via passlib
- **File Handling**: aiofiles for async operations
- **Validation**: Pydantic v2

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- pip

### Setup Steps

1. **Clone or access the project directory**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create environment file**
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
DATABASE_URL=sqlite:///./holabox.db
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
STORAGE_PATH=./storage
```

4. **Create storage directory**
```bash
mkdir -p storage
```

5. **Run the server**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

The API will be available at: `http://localhost:5000`

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:5000/docs`
- **ReDoc**: `http://localhost:5000/redoc`

## 🔑 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login user |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/change-password` | Change password |
| POST | `/auth/logout` | Logout user |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get current user profile |
| PUT | `/users/me` | Update user profile |
| GET | `/users/storage` | Get storage information |

### Storage

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/storage/folders` | Create folder |
| GET | `/storage/folders` | List folders |
| POST | `/storage/upload` | Upload file |
| GET | `/storage/files` | List files |
| GET | `/storage/files/{id}/download` | Download file |
| DELETE | `/storage/files/{id}` | Delete file (soft delete) |
| POST | `/storage/files/{id}/restore` | Restore from trash |
| PUT | `/storage/files/{id}/rename` | Rename file |

### Sharing

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shares/` | Create share link |
| GET | `/shares/my-shares` | List user's shares |
| GET | `/shares/{token}/access` | Access shared file info |
| GET | `/shares/{token}/download` | Download shared file |
| DELETE | `/shares/{id}` | Delete share |

### Premium

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/premium/plans` | Get available plans |
| POST | `/premium/upgrade` | Upgrade to premium plan |
| GET | `/premium/subscription` | Get current subscription |

### Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/users` | List all users |
| POST | `/admin/users/{id}/suspend` | Suspend user |
| POST | `/admin/users/{id}/activate` | Activate user |
| POST | `/admin/users/{id}/reset-storage` | Recalculate storage |
| GET | `/admin/stats` | Get server statistics |

## 💡 Usage Examples

### 1. Register a New User

```bash
curl -X POST "http://localhost:5000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "SecurePass123",
    "full_name": "Test User"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Login

```bash
curl -X POST "http://localhost:5000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

### 3. Upload a File

```bash
curl -X POST "http://localhost:5000/storage/upload" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/file.pdf"
```

### 4. Create a Folder

```bash
curl -X POST "http://localhost:5000/storage/folders" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Documents",
    "parent_id": null
  }'
```

### 5. Create a Share Link

```bash
curl -X POST "http://localhost:5000/shares/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": 1,
    "password": "optional_password",
    "expiry_hours": 24
  }'
```

### 6. Upgrade to Premium

```bash
curl -X POST "http://localhost:5000/premium/upgrade" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_type": "premium",
    "payment_method": "credit_card"
  }'
```

## 🗄️ Database Schema

The application uses the following main models:

- **User**: User accounts with authentication and plan information
- **File**: File metadata and storage references
- **Folder**: Folder hierarchy and organization
- **Share**: Public sharing links with access control
- **Subscription**: Premium plan subscriptions

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Token expiration and refresh mechanism
- Password-protected shares
- User-based file access control
- Admin-only endpoints

## 📁 Project Structure

```
holabox-backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config/
│   │   ├── database.py         # Database configuration
│   │   └── settings.py         # Application settings
│   ├── auth/
│   │   ├── routes.py           # Authentication endpoints
│   │   ├── jwt_handler.py      # JWT token management
│   │   └── hashing.py          # Password hashing
│   ├── users/
│   │   ├── routes.py           # User endpoints
│   │   ├── models.py           # User database model
│   │   └── service.py          # User business logic
│   ├── storage/
│   │   ├── routes.py           # Storage endpoints
│   │   ├── service.py          # Storage business logic
│   │   └── utils.py            # Storage utilities
│   ├── sharing/
│   │   ├── routes.py           # Sharing endpoints
│   │   ├── models.py           # Share database model
│   │   └── service.py          # Sharing business logic
│   ├── premium/
│   │   ├── routes.py           # Premium endpoints
│   │   └── models.py           # Subscription model
│   ├── admin/
│   │   └── routes.py           # Admin endpoints
│   ├── common/
│   │   ├── models.py           # Shared database models
│   │   ├── helpers.py          # Utility functions
│   │   └── storage_engine.py  # File storage engine
│   └── schemas/
│       ├── user_schema.py      # User Pydantic schemas
│       ├── file_schema.py      # File Pydantic schemas
│       ├── auth_schema.py      # Auth Pydantic schemas
│       └── share_schema.py     # Share Pydantic schemas
├── storage/                     # File storage directory
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🚀 Production Deployment

For production deployment:

1. **Use PostgreSQL instead of SQLite**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/holabox
```

2. **Set a strong SECRET_KEY**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

3. **Configure CORS properly** in `app/main.py`

4. **Use a production ASGI server**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --workers 4
```

5. **Set up file storage** (MinIO, S3, or persistent volume)

6. **Enable HTTPS** with reverse proxy (nginx/caddy)

## 📊 Storage Limits

| Plan | Storage | Price |
|------|---------|-------|
| Free | 20 GB | $0 |
| Premium | 1 TB | $9.99/month |
| Ultra | 2 TB | $19.99/month |

## 🧪 Testing

Create a test user and admin account by registering through the API:

**Regular User:**
```json
{
  "email": "user@holabox.com",
  "username": "testuser",
  "password": "Test123!",
  "full_name": "Test User"
}
```

**Admin User** (manually set `is_admin=True` in database):
```sql
UPDATE users SET is_admin = 1 WHERE email = 'admin@holabox.com';
```

## ⚠️ Known Limitations

The current implementation has some areas that could be enhanced for production use:

1. **File Upload**: Files are currently loaded entirely into memory before saving. For very large files (>1GB), implement chunked/streaming uploads with size validation before reading entire content.

2. **Storage Quota Edge Cases**: While basic quota enforcement is implemented, complex scenarios involving admin storage resets combined with concurrent operations may result in temporary quota inconsistencies. For production, implement database-level locks and real-time recalculation.

3. **Token Management**: JWT tokens remain valid even after password changes. Implement Redis-based token blacklisting or rotation on security-sensitive operations for production use.

4. **File Streaming**: Downloads use FileResponse. For large video files, implement range request support (HTTP 206) for proper streaming and seeking.

5. **Admin Metrics**: Admin stats show active storage only. For complete visibility, add separate metrics for trashed files and total disk usage.

6. **Database**: Current default is SQLite. For production with multiple concurrent users, switch to PostgreSQL and implement proper transaction isolation.

## 🤝 Contributing

This is a production-grade backend implementation. Suggested improvements:

- Email verification system
- Forgot password with email reset
- Redis caching for file metadata and token blacklist
- MinIO or S3 integration for scalable object storage
- Chunked upload support with resume capability
- Image thumbnail generation and optimization
- Video streaming with range request support
- Automated trash cleanup job (30-day permanent deletion)
- Comprehensive test suite with unit and integration tests
- Rate limiting and request throttling
- Audit logs for security and compliance
- Database migrations with Alembic

## 📝 License

This project is built for educational and commercial use.

## 🆘 Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Review the server logs for errors
3. Ensure all dependencies are installed
4. Verify database connection
5. Check file system permissions for `storage/` directory

---

**Built with ❤️ using FastAPI and Python**
