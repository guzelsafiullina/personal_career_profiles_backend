import os
import pathlib
from ast import In
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

ROOT_DIR = pathlib.Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
DB_URL = os.getenv("DB_URL")

Base = declarative_base()

def get_user(username: str):
    """Return user info from database"""
    results = session.query(Person).filter(Person.username == username)
    for r in results:
        return r.__dict__


class Person(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column("username", String)
    pass_hash = Column("pass_hash", String)
   
    def __init__(self, username, pass_hash):
        self.username = username
        self.pass_hash = pass_hash

    

engine = create_engine(
    DB_URL,
    isolation_level = "REPEATABLE READ"
)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

