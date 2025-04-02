import sqlalchemy as sql
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = sql.create_engine(DATABASE_URL)
SessionLocal = sql.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = sql.orm.declarative_base()
