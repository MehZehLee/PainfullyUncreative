from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'Tasks'
    task_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text)
    status = Column(String, default='Open')
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)
