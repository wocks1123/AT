from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import settings


DATABASE = 'sqlite:///./database.db'


engine = create_engine(
    DATABASE,
    echo=settings.DB_ECHO,
    connect_args={"check_same_thread": False}
)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit=settings.AUTO_COMMIT,
        autoflush=False,
        bind=engine
    )
)
