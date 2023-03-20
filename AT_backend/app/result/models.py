from sqlalchemy import Column, Integer, String

from app.db import Base


class Result(Base):
    id = Column(Integer, primary_key=True)
    start_timestamp = Column(String)
    end_timestamp = Column(String)
    video_path = Column(String)
