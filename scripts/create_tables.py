"""Create all tables defined in SQLAlchemy models by calling Base.metadata.create_all.

This script uses the same settings as the app (reads `.env`) and will create tables
directly in the configured database (Postgres Neon in your `.env`).
"""
from app.config.database import engine, Base


def main():
    print("Creating tables using engine:", engine)
    Base.metadata.create_all(bind=engine)
    print("Tables created (if not present).")


if __name__ == '__main__':
    main()
