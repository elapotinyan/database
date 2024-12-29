from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Gosudarstvo, Natsionalnost, Naselenie
from schemas import GosudarstvoCreate, Gosudarstvo, NatsionalnostCreate, Natsionalnost, NaselenieCreate, Naselenie

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/gosudarstvo/", response_model=Gosudarstvo)
def create_gosudarstvo(gosudarstvo: GosudarstvoCreate, db: Session = Depends(get_db)):
    if db.query(Gosudarstvo).filter(Gosudarstvo.name == gosudarstvo.name).first():
        raise HTTPException(status_code=400, detail="Gosudarstvo already exists")
    db_gosudarstvo = Gosudarstvo(**gosudarstvo.dict())
    db.add(db_gosudarstvo)
    db.commit()
    db.refresh(db_gosudarstvo)
    return db_gosudarstvo

@app.post("/natsionalnost/", response_model=Natsionalnost)
def create_natsionalnost(natsionalnost: NatsionalnostCreate, db: Session = Depends(get_db)):
    # Проверка на уникальность имени
    if db.query(Natsionalnost).filter(Natsionalnost.name == natsionalnost.name).first():
        raise HTTPException(status_code=400, detail="Natsionalnost already exists")
    db_natsionalnost = Natsionalnost(**natsionalnost.dict())
    db.add(db_natsionalnost)
    db.commit()
    db.refresh(db_natsionalnost)
    return db_natsionalnost

@app.post("/naselenie/", response_model=Naselenie)
def create_naselenie(naselenie: NaselenieCreate, db: Session = Depends(get_db)):
    # Проверка на существование связей
    if not db.query(Gosudarstvo).filter(Gosudarstvo.id == naselenie.gosudarstvo_id).first():
        raise HTTPException(status_code=404, detail="Gosudarstvo not found")
    if not db.query(Natsionalnost).filter(Natsionalnost.id == naselenie.natsionalnost_id).first():
        raise HTTPException(status_code=404, detail="Natsionalnost not found")
    
    
    db_naselenie = Naselenie(**naselenie.dict())
    db.add(db_naselenie)
    db.commit()
    db.refresh(db_naselenie)
    return db_naselenie

@app.get("/natsionalnost/", response_model=list[Natsionalnost])
def get_all_natsionalnost(db: Session = Depends(get_db)):
   
    return db.query(Natsionalnost).all()

@app.get("/natsionalnost/{natsionalnost_id}", response_model=Natsionalnost)
def get_natsionalnost_by_id(natsionalnost_id: int, db: Session = Depends(get_db)):
    
    natsionalnost = db.query(Natsionalnost).filter(Natsionalnost.id == natsionalnost_id).first()
    if not natsionalnost:
        raise HTTPException(status_code=404, detail="Natsionalnost not found")
    return natsionalnost

@app.get("/naselenie/", response_model=list[Naselenie])
def get_all_naselenie(db: Session = Depends(get_db)):
    
    return db.query(Naselenie).all()

@app.get("/naselenie/{naselenie_id}", response_model=Naselenie)
def get_naselenie_by_id(naselenie_id: int, db: Session = Depends(get_db)):
   
    naselenie = db.query(Naselenie).filter(Naselenie.id == naselenie_id).first()
    if not naselenie:
        raise HTTPException(status_code=404, detail="Naselenie not found")
    return naselenie