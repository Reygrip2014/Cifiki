from datetime import datetime

from sqlalchemy import Column, Boolean, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Site(Base):
    __tablename__ = "site"
    
    id = Column(Integer,primary_key=True)
    url = Column(String(100))
    name = Column(String(50))
    main_news_id = Column(Integer, default=-1)
    news = relationship("News", back_populates="site")

class News(Base):
    __tablename__ = "news"

    id = Column(Integer,primary_key=True)
    url = Column(String(100))
    is_main = Column(Boolean, default=True)
    start = Column(DateTime)
    stop = Column(DateTime, default=datetime(1, 1, 1, 0, 0))
    site_id = Column(Integer, ForeignKey("site.id"))
    site = relationship("Site", back_populates="news")
