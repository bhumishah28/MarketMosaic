"""Environment-driven SQLAlchemy connection management for MySQL 8.x."""

from __future__ import annotations

import logging
import os
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from dotenv import load_dotenv
from sqlalchemy import URL, Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DatabaseSettings:
    """Connection settings loaded from environment variables."""

    host: str = "127.0.0.1"
    port: int = 3306
    database: str = "marketmosaic"
    user: str = "marketmosaic"
    password: str = ""
    pool_size: int = 5
    max_overflow: int = 10

    @classmethod
    def from_env(cls) -> DatabaseSettings:
        load_dotenv()
        return cls(
            host=os.getenv("MYSQL_HOST", cls.host),
            port=int(os.getenv("MYSQL_PORT", cls.port)),
            database=os.getenv("MYSQL_DATABASE", cls.database),
            user=os.getenv("MYSQL_USER", cls.user),
            password=os.getenv("MYSQL_PASSWORD", ""),
            pool_size=int(os.getenv("MYSQL_POOL_SIZE", cls.pool_size)),
            max_overflow=int(os.getenv("MYSQL_MAX_OVERFLOW", cls.max_overflow)),
        )

    @property
    def url(self) -> URL:
        return URL.create(
            "mysql+pymysql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            query={"charset": "utf8mb4"},
        )


def create_database_engine(settings: DatabaseSettings | None = None) -> Engine:
    """Create a pooled MySQL engine without exposing credentials in logs."""
    config = settings or DatabaseSettings.from_env()
    return create_engine(
        config.url,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_size=config.pool_size,
        max_overflow=config.max_overflow,
        future=True,
    )


def test_connection(engine: Engine) -> bool:
    """Return whether a simple MySQL query succeeds, logging useful failures."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("MySQL connection test succeeded")
        return True
    except SQLAlchemyError:
        logger.exception("MySQL connection test failed")
        return False


@contextmanager
def connection_scope(engine: Engine) -> Iterator[object]:
    """Yield a connection and ensure it is returned to the pool."""
    with engine.connect() as connection:
        yield connection
