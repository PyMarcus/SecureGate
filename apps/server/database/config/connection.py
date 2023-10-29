from pathlib import Path
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from apps.server.database.models import BaseModel
from libs import LogMaker
from packages.config.env import env


class DBConnection:
    __engine: Optional[Engine] = None

    @classmethod
    def __db_connection(cls, sqlite: bool = False) -> Engine | None:
        if cls.__engine:
            return

        if sqlite:
            file_db: str = "database/items.db"
            folder: Path = Path(file_db).parent
            folder.mkdir(parents=True, exist_ok=True)
            conn_str: str = f"sqlite:///{file_db}"
            cls.__engine = sa.create_engine(
                url=conn_str, echo=False, connect_args={"check_same_thread": False}
            )

        else:
            db_url = env.DATABASE_URL
            if not db_url:
                raise Exception("DATABASE_URL not set")

            cls.__engine = sa.create_engine(url=db_url, echo=False)
        LogMaker.write_log("[+]Connected on database", "info")
        return cls.__engine

    @classmethod
    def create_session(cls) -> Session:
        if not cls.__engine:
            cls.__db_connection()

        session: sessionmaker = sessionmaker(cls.__engine, expire_on_commit=False, class_=Session)
        return session()

    @classmethod
    def create_tables(cls) -> None:
        if not cls.__engine:
            cls.__db_connection()

        LogMaker.write_log("[+]Drop all tables", "info")
        # BaseModel.metadata.drop_all(cls.__engine)
        LogMaker.write_log("[+]Create all tables", "info")
        BaseModel.metadata.create_all(cls.__engine)
        LogMaker.write_log("[+]OK", "info")
