# database.py
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os
from datetime import datetime

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    passport = Column(String(50))
    orders = relationship("Order", back_populates="client")

class Tour(Base):
    __tablename__ = 'tours'
    id = Column(Integer, primary_key=True)
    destination = Column(String(100))
    start_date = Column(Date)
    duration = Column(Integer)
    price = Column(Integer)
    operator = Column(String(100))
    adults = Column(Integer, default=1)
    children = Column(Integer, default=0)
    orders = relationship("Order", back_populates="tour")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'))
    tour_id = Column(Integer, ForeignKey('tours.id', ondelete='CASCADE'))
    status = Column(String(20), default='В работе')
    client = relationship("Client", back_populates="orders")
    tour = relationship("Tour", back_populates="orders")

class Database:
    def __init__(self):
        db_dir = 'data'
        db_file = 'tour_manager.db'
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, db_file)
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()