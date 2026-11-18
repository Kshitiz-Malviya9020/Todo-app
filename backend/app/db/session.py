from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Construct the database URL safely.
# URL.create handles special characters in passwords.
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD.get_secret_value(),
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
    query={"charset": "utf8mb4"},
)


# Create the SQLAlchemy engine.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# Create a session factory.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# FastAPI database dependency.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
