from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
from config import USER_NAME, USER_PASSWORD, DB_HOST, DB_PORT, DB_NAME


engine = create_engine(f'postgresql+psycopg2://{USER_NAME}:{USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Apartments(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    currency_type = Column(String)
    location = Column(String)
    descr = Column(String)
    bedrooms = Column(String)
    image_url = Column(String)
    date = Column(String)

    def __init__(self, dct: dict):
        self.title = dct['title']
        self.price = 0.0 if dct['price'] is None else float(dct['price'])
        self.currency_type = 0.0 if dct['currency_type'] is None else dct['currency_type']
        self.location = dct['location']
        self.descr = dct['descr']
        self.bedrooms = dct['bedrooms']
        self.image_url = dct['image_url']
        self.date = dct['date']

    def __repr__(self):
        info: str = f'{self.title}, {self.currency_type + self.price}, {self.location}, {self.descr}, {self.bedrooms}\
                    {self.image_url}, {self.date}'
        return info


def create_db() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def push_data_to_db(data: list) -> None:
    create_db()
    session = Session()

    for item in data:
        row = Apartments(item)
        session.add(row)

    session.commit()
    session.close()
    print('Saving data to the database was successful!')