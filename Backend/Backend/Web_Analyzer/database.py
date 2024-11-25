from sqlalchemy import create_engine, Column, Integer, Text, String, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime


DATABASE_URL = "postgresql://postgres:animesh006@localhost/seo_ads_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ScrapedContent(Base):
    __tablename__ = "scraped_content"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, unique=True, index=True)
    html_elements = Column(Text)
    elements_properties = Column(JSON)
    css = Column(Text)
    body_content = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    user_details = Column(Text)
    sub_details = Column(Text)
    profession = Column(String)
    days_left = Column(Integer, default=30)
    image = Column(Text, nullable=True)  # This will store the path or name of the image
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"
    report_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    feature = Column(String, index=True)
    sub_feature = Column(String, index=True)
    date = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    data = Column(JSON)  # JSON column to store report data

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
