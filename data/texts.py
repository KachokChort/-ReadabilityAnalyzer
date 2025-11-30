from sqlalchemy import Column, Integer, String, DateTime, JSON
from .db_session import Base
import datetime


class Text(Base):
    __tablename__ = 'texts'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    user = Column(String(50), nullable=False)
    text = Column(String(), nullable=False)
    score = Column(String(150), nullable=False)
    level = Column(String(150), nullable=False)
    sentences = Column(String(150), nullable=False)
    words_per_sentence = Column(String(150), nullable=False)
    reading_time = Column(String(150), nullable=False)
    words = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    recommendations = Column(JSON)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self. name
