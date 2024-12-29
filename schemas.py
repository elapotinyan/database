from pydantic import BaseModel
from typing import Optional

class GosudarstvoBase(BaseModel):
    name: str
    capital: Optional[str] = None
    governance: Optional[str] = None

class GosudarstvoCreate(GosudarstvoBase):
    pass

class Gosudarstvo(GosudarstvoBase):
    id: int
    class Config:
        orm_mode = True

class NatsionalnostBase(BaseModel):
    name: str
    language: Optional[str] = None
    total_population: Optional[int] = None

class NatsionalnostCreate(NatsionalnostBase):
    pass

class Natsionalnost(NatsionalnostBase):
    id: int
    class Config:
        orm_mode = True

class NaselenieBase(BaseModel):
    male: Optional[int] = None
    female: Optional[int] = None
    total: Optional[int] = None

class NaselenieCreate(NaselenieBase):
    gosudarstvo_id: int
    natsionalnost_id: int

class Naselenie(NaselenieBase):
    id: int
    gosudarstvo_id: int
    natsionalnost_id: int
    class Config:
        orm_mode = True
