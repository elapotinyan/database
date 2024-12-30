from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import SessionLocal, State, Nationality, Population
from schemas import StateCreate, StateSchema, NationalityCreate, NationalitySchema, PopulationCreate, PopulationSchema

app = FastAPI()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create - создание новой записи для Государства
@app.post("/states/", response_model=StateSchema)
def create_state(state: StateCreate, db: Session = Depends(get_db)):
    db_state = State(name=state.name, capital=state.capital, government_type=state.government_type)
    db.add(db_state)
    db.commit()
    db.refresh(db_state)
    return db_state

# Read - получение списка всех Государств
@app.get("/states/", response_model=list[StateSchema])
def get_states(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    states = db.query(State).offset(skip).limit(limit).all()
    return states

# Read - получение записи Государства по ID
@app.get("/states/{state_id}", response_model=StateSchema)
def get_state(state_id: int, db: Session = Depends(get_db)):
    state = db.query(State).filter(State.id == state_id).first()
    if not state:
        raise HTTPException(status_code=404, detail="State not found")
    return state

@app.put("/states/{state_id}", response_model=StateSchema)
def update_state(state_id: int, state: StateCreate, db: Session = Depends(get_db)):
    db_state = db.query(State).filter(State.id == state_id).first()
    if db_state is None:
        raise HTTPException(status_code=404, detail="State not found")
    
    db_state.name = state.name
    db_state.capital = state.capital
    db_state.government_type = state.government_type
    
    db.commit()
    db.refresh(db_state)
    return db_state

# Delete - удаление записи Государства
@app.delete("/states/{state_id}", response_model=StateSchema)
def delete_state(state_id: int, db: Session = Depends(get_db)):
    db_state = db.query(State).filter(State.id == state_id).first()
    if db_state is None:
        raise HTTPException(status_code=404, detail="State not found")
    
    db.delete(db_state)
    db.commit()
    return db_state
# Create - создание новой записи для Национальности
@app.post("/nationalities/", response_model=NationalitySchema)
def create_nationality(nationality: NationalityCreate, db: Session = Depends(get_db)):
    db_nationality = Nationality(name=nationality.name, language=nationality.language, total_population=nationality.total_population)
    db.add(db_nationality)
    db.commit()
    db.refresh(db_nationality)
    return db_nationality

# Read - получение списка всех Национальностей
@app.get("/nationalities/", response_model=list[NationalitySchema])
def get_nationalities(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    nationalities = db.query(Nationality).offset(skip).limit(limit).all()
    return nationalities

# Read - получение записи Национальности по ID
@app.get("/nationalities/{nationality_id}", response_model=NationalitySchema)
def get_nationality(nationality_id: int, db: Session = Depends(get_db)):
    nationality = db.query(Nationality).filter(Nationality.id == nationality_id).first()
    if not nationality:
        raise HTTPException(status_code=404, detail="Nationality not found")
    return nationality

@app.put("/nationalities/{nationality_id}", response_model=NationalitySchema)
def update_nationality(nationality_id: int, nationality: NationalityCreate, db: Session = Depends(get_db)):
    db_nationality = db.query(Nationality).filter(Nationality.id == nationality_id).first()
    if db_nationality is None:
        raise HTTPException(status_code=404, detail="Nationality not found")
    
    db_nationality.name = nationality.name
    db_nationality.language = nationality.language
    db_nationality.total_population = nationality.total_population
    
    db.commit()
    db.refresh(db_nationality)
    return db_nationality

@app.delete("/nationalities/{nationality_id}", response_model=NationalitySchema)
def delete_nationality(nationality_id: int, db: Session = Depends(get_db)):
    db_nationality = db.query(Nationality).filter(Nationality.id == nationality_id).first()
    if db_nationality is None:
        raise HTTPException(status_code=404, detail="Nationality not found")
    
    db.delete(db_nationality)
    db.commit()
    return db_nationality
# Create - создание новой записи для Населения
@app.post("/populations/", response_model=PopulationSchema)
def create_population(population: PopulationCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли state с указанным state_id
    db_state = db.query(State).filter(State.id == population.state_id).first()
    if db_state is None:
        raise HTTPException(status_code=404, detail="State not found")

    # Проверяем, существует ли nationality с указанным nationality_id
    db_nationality = db.query(Nationality).filter(Nationality.id == population.nationality_id).first()
    if db_nationality is None:
        raise HTTPException(status_code=404, detail="Nationality not found")

    db_population = Population(
        state_id=population.state_id,
        nationality_id=population.nationality_id,
        male_population=population.male_population,
        female_population=population.female_population,
        total_population=population.total_population
    )
    
    try:
        db.add(db_population)
        db.commit()
        db.refresh(db_population)
    except Exception as e:
        db.rollback()  # Откатываем изменения в случае ошибки
        raise HTTPException(status_code=500, detail=f"Error creating population: {str(e)}")

    return db_population


# Read - получение списка всех записей Населения
@app.get("/populations/", response_model=list[PopulationSchema])
def get_populations(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    populations = db.query(Population).offset(skip).limit(limit).all()
    return populations

# Read - получение записи Населения по ID
@app.get("//{population_id}", response_model=PopulationSchema)
def get_population(population_id: int, db: Session = Depends(get_db)):
    population = db.query(Population).filter(Population.id == population_id).first()
    if not population:
        raise HTTPException(status_code=404, detail="Population not found")
    return population

@app.put("/populations/{population_id}", response_model=PopulationSchema)
def update_population(population_id: int, population: PopulationCreate, db: Session = Depends(get_db)):
    db_population = db.query(Population).filter(Population.id == population_id).first()
    if db_population is None:
        raise HTTPException(status_code=404, detail="Population not found")
    
    db_population.state_id = population.state_id
    db_population.nationality_id = population.nationality_id
    db_population.male_population = population.male_population
    db_population.female_population = population.female_population
    db_population.total_population = population.total_population
    
    db.commit()
    db.refresh(db_population)
    return db_population

@app.delete("/populations/{population_id}", response_model=PopulationSchema)
def delete_population(population_id: int, db: Session = Depends(get_db)):
    db_population = db.query(Population).filter(Population.id == population_id).first()
    if db_population is None:
        raise HTTPException(status_code=404, detail="Population not found")
    
    db.delete(db_population)
    db.commit()
    return db_population