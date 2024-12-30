from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:1111@localhost:5432/geograph_db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class State(Base):
    __tablename__ = 'states'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    capital = Column(String)
    government_type = Column(String)

    populations = relationship("Population", back_populates="state")

class Nationality(Base):
    __tablename__ = 'nationalities'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    language = Column(String)
    total_population = Column(Integer)

    populations = relationship("Population", back_populates="nationality")

class Population(Base):
    __tablename__ = 'populations'

    id = Column(Integer, primary_key=True)
    state_id = Column(Integer, ForeignKey('states.id'))
    nationality_id = Column(Integer, ForeignKey('nationalities.id'))
    male_population = Column(Integer)
    female_population = Column(Integer)
    total_population = Column(Integer)

    state = relationship("State", back_populates="populations")
    nationality = relationship("Nationality", back_populates="populations")

Base.metadata.create_all(bind=engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
