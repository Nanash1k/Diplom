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
    notes = Column(String(500))


class Tour(Base):
    __tablename__ = 'tours'
    id = Column(Integer, primary_key=True)
    destination = Column(String(100))
    start_date = Column(Date)  # Исправлено: удалена лишняя скобка
    duration = Column(Integer)  # Исправлено
    price = Column(Integer)  # Исправлено
    operator = Column(String(100))


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    tour_id = Column(Integer, ForeignKey('tours.id'))
    status = Column(String(20), default='В работе')

    client = relationship("Client")
    tour = relationship("Tour")


class Database:
    def __init__(self):
        db_dir = 'data'
        db_file = 'tour_manager.db'

        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        db_path = os.path.join(db_dir, db_file)
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self._seed_initial_data()

    def _seed_initial_data(self):
        if not self.session.query(Client).first():
            clients = [
                Client(name="Иванов Иван", phone="+79111234567", email="ivanov@mail.ru"),
                Client(name="Петрова Мария", phone="+79219876543", email="petrova@mail.ru")
            ]

            tours = [
                Tour(
                    destination="Мальдивы",
                    start_date=datetime(2024, 9, 15),
                    duration=10,
                    price=150000
                ),
                Tour(
                    destination="Турция",
                    start_date=datetime(2024, 7, 1),
                    duration=7,
                    price=80000
                )
            ]

            orders = [
                Order(client_id=1, tour_id=1, status="Подтвержден"),
                Order(client_id=2, tour_id=2, status="В работе")
            ]

            self.session.add_all(clients + tours + orders)
            self.session.commit()