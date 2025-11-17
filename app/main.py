from fastapi import FastAPI
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
    init_db()


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
