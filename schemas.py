from pydantic import BaseModel

# Схемы для Государства
class StateBase(BaseModel):
    name: str
    capital: str
    government_type: str

class StateCreate(StateBase):
    pass

class StateSchema(StateBase):
    id: int

    class Config:
        orm_mode = True

# Схемы для Национальности
class NationalityBase(BaseModel):
    name: str
    language: str
    total_population: int

class NationalityCreate(NationalityBase):
    pass

class NationalitySchema(NationalityBase):
    id: int

    class Config:
        orm_mode = True

# Схемы для Населения
class PopulationBase(BaseModel):
    state_id: int
    nationality_id: int
    male_population: int
    female_population: int
    total_population: int

class PopulationCreate(PopulationBase):
    pass

class PopulationSchema(PopulationBase):
    id: int

    class Config:
        orm_mode = True
