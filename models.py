from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Gosudarstvo(Base):
    __tablename__ = 'gosudarstvo'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    capital = Column(String, nullable=True)
    governance = Column(String, nullable=True)
    population = relationship("Naselenie", back_populates="gosudarstvo")

class Natsionalnost(Base):
    __tablename__ = 'natsionalnost'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    language = Column(String, nullable=True)
    total_population = Column(Integer, nullable=True)
    population = relationship("Naselenie", back_populates="natsionalnost")

class Naselenie(Base):
    __tablename__ = 'naselenie'
    id = Column(Integer, primary_key=True, index=True)
    gosudarstvo_id = Column(Integer, ForeignKey("gosudarstvo.id"), nullable=False)
    natsionalnost_id = Column(Integer, ForeignKey("natsionalnost.id"), nullable=False)
    male = Column(Integer, nullable=True)
    female = Column(Integer, nullable=True)
    total = Column(Integer, nullable=True)
    gosudarstvo = relationship("Gosudarstvo", back_populates="population")
    natsionalnost = relationship("Natsionalnost", back_populates="population")
