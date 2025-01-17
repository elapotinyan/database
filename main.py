from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import SessionLocal, State, Nationality, Population
from schemas import StateCreate, StateSchema, NationalityCreate, NationalitySchema, PopulationCreate, PopulationSchema
from typing import Optional
from sqlalchemy import func
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/states/", response_model=StateSchema)
def create_state(state: StateCreate, db: Session = Depends(get_db)):
    db_state = State(name=state.name, capital=state.capital, government_type=state.government_type)
    db.add(db_state)
    db.commit()
    db.refresh(db_state)
    return db_state


@app.get("/states/", response_model=list[StateSchema])
def get_states(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    states = db.query(State).offset(skip).limit(limit).all()
    return states


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

@app.delete("/states/{state_id}", response_model=StateSchema)
def delete_state(state_id: int, db: Session = Depends(get_db)):
    db_state = db.query(State).filter(State.id == state_id).first()
    if db_state is None:
        raise HTTPException(status_code=404, detail="State not found")
    
    db.delete(db_state)
    db.commit()
    return db_state

@app.post("/nationalities/", response_model=NationalitySchema)
def create_nationality(nationality: NationalityCreate, db: Session = Depends(get_db)):
    db_nationality = Nationality(name=nationality.name, language=nationality.language, total_population=nationality.total_population)
    db.add(db_nationality)
    db.commit()
    db.refresh(db_nationality)
    return db_nationality


@app.get("/nationalities/", response_model=list[NationalitySchema])
def get_nationalities(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    nationalities = db.query(Nationality).offset(skip).limit(limit).all()
    return nationalities

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

@app.post("/populations/", response_model=PopulationSchema)
def create_population(population: PopulationCreate, db: Session = Depends(get_db)):
   
    db_state = db.query(State).filter(State.id == population.state_id).first()
    if db_state is None:
        raise HTTPException(status_code=404, detail="State not found")

   
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
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"Error creating population: {str(e)}")

    return db_population



@app.get("/populations/", response_model=list[PopulationSchema])
def get_populations(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    populations = db.query(Population).offset(skip).limit(limit).all()
    return populations

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


@app.get("/states/join/", response_model=list[StateSchema])
def get_states_by_population(
    population_threshold: int, 
    db: Session = Depends(get_db)
):

    states = db.query(State).join(Population).filter(
        Population.total_population > population_threshold
    ).all()
    
    if not states:
        raise HTTPException(
            status_code=404,
            detail=f"No states found with population over {population_threshold}"
        )
    
    return states


@app.get("/states/select/", response_model=list[StateSchema])
def search_states_by_capital_and_government(
    capital: str, 
    government_type: str, 
    db: Session = Depends(get_db)
):
    
    states = db.query(State).filter(
        State.capital == capital,
        State.government_type == government_type
    ).all()

    if not states:
        raise HTTPException(
            status_code=404,
            detail=f"No states found with capital '{capital}' and government type '{government_type}'"
        )

    return states

@app.put("/nationalities/update/", response_model=list[NationalitySchema])
def update_nationalities_by_language(
    language: str, 
    new_total_population: int, 
    db: Session = Depends(get_db)
):
    nationalities = db.query(Nationality).filter(
        Nationality.language == language
    ).all()

    if not nationalities:
        raise HTTPException(
            status_code=404,
            detail=f"No nationalities found with language '{language}'"
        )

    for nationality in nationalities:
        nationality.total_population = new_total_population
        db.commit()
        db.refresh(nationality)

    return nationalities


@app.get("/populations/group_by/")
def group_populations_by_state(
    state_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    
    query = db.query(
        Population.state_id,
        func.sum(Population.male_population).label("total_male_population"),
        func.sum(Population.female_population).label("total_female_population"),
        func.sum(Population.total_population).label("total_population"),
        (func.sum(Population.male_population) * 100.0 / func.sum(Population.total_population)).label("male_percentage")
    )
    
    if state_id:
        query = query.filter(Population.state_id == state_id)
    
    query = query.group_by(Population.state_id)
    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="No population data found for grouping by state.")
    
    return [
        {
            "state_id": result.state_id,
            "total_male_population": result.total_male_population,
            "total_female_population": result.total_female_population,
            "total_population": result.total_population,
            "male_percentage": round(result.male_percentage, 2)
        }
        for result in results
    ]