from typing import Union, Optional, List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
#from .models import Item
#from .calcul import calc_int

app = FastAPI(title="Integration With SQL")

# --- DataBase Setup
engine = create_engine("sqlite:///./patients.db", connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class patient_model(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(Integer)
    pressurehight = Column(Integer)
    pressurelow = Column(Integer)
    glucose = Column(Integer)
    kcm = Column(Integer)
    troponin = Column(Integer)
    impluse = Column(Integer)

Base.metadata.create_all(engine)

# --- pydantic Models (DataClass)
class PatientResponse(BaseModel):
    name : str
    age : int
    gender: int
    pressurehight: float
    pressurelow: float
    glucose: float
    kcm: float
    troponin: float
    impluse: float

class Config:
    from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#get_db()

# --- endpoint à la racine
@app.get('/')
def read_root():
    return {"message" : "bienvenue sur mon API"}

@app.get("/Patients/", response_model=PatientResponse)
def get_patients(user_id:int, db:Session=Depends(get_db)):
    Patients = db.query(patient_model).all()
    if not Patients:
        raise HTTPException(status_code=404, detail="Patient Not Found")
    return Patients

@app.post("/users/", response_model=PatientResponse)
def add_patient(patient: patient_model, db:Session=Depends(get_db)):
    if db.query(patient_model):
        raise HTTPException(status_code=44, detail="User already exists !")
    # Create a new user
    new_patient = patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


"""
#Update user
@app.put("/user/{user_id}", response_model=UserResponse)
def update_user(user_id:int, user:UserCreate, db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User already exists ! ")
    
    for field, value in user.dict().item():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

#delete user
@app.delete("/users/{user_id}")
def delete_user(user_id:int,db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User already exists ! ")
    
    db.delete(db_user)
    db.commit()
    return db_user

# ---  Get All Users
@app.get("/users/", response_model=List[UserResponse])
def get_all_users(db:Session=Depends(get_db)):
    return db.query(User).all()


@app.get("/items/{item_id}")
async def read_item(item_id : int, q : Union[str, None] = None):
    return {"item_id" : item_id, "q" : q}


@app.get("/get_cal")
def get_cal(a:int, b:int, opt:str):
    return {"resultat" : calc_int(a,b,opt)}
#endpoint : ressource 'item'

app.get('/Items')
def get_all_items():
    return {"msg" : " lister tous les items "}"""

