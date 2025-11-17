from fastapi import FastAPI
import os
import logging
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import init_db
from app.auth import routes as auth_routes
from app.users import routes as user_routes
from app.storage import routes as storage_routes
from app.sharing import routes as sharing_routes
from app.premium import routes as premium_routes
from app.admin import routes as admin_routes

app = FastAPI(
    title="HolaBox API",
    description="Cloud Storage API similar to TeraBox",
    version="1.0.0"
)

# configure logging to file for unhandled exceptions
logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'error.log'),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(storage_routes.router)
app.include_router(sharing_routes.router)
app.include_router(premium_routes.router)
app.include_router(admin_routes.router)


@app.on_event("startup")
def startup_event():
    """Initialize DB on startup unless SKIP_DB env var is set.

    This allows running the app without an available database for
    local testing or CI where DB isn't required.
    """
    skip_db = os.environ.get("SKIP_DB", "0").lower() in ("1", "true", "yes")
    if skip_db:
        logging.info("SKIP_DB set — skipping database initialization")
        return

    try:
        init_db()
    except Exception:
        logging.exception("Database initialization failed. Continuing without DB because SKIP_DB is not set.")


from fastapi.responses import JSONResponse
from fastapi.requests import Request


@app.get("/")
def read_root():
    return {
        "message": "Welcome to HolaBox API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.exception("Unhandled exception during request: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
