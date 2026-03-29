from typing import Union, Optional, List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
#from .models import Item
#from .calcul import calc_int

app = FastAPI(title="Cardio Risk API")

# --- DataBase Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./patients.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class patient_model(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(Integer)
    pressurehight = Column(Float)
    pressurelow = Column(Float)
    glucose = Column(Float)
    kcm = Column(Float)
    troponin = Column(Float)
    impluse = Column(Float)

Base.metadata.create_all(engine)

# --- pydantic Models (DataClass)
class PatientCreate(BaseModel):
    name : str
    age : int
    gender: int
    pressurehight: float
    pressurelow: float
    glucose: float
    kcm: float
    troponin: float
    impluse: float
    
# Schéma pour la RÉPONSE (ce que l'API renvoie)
# Il inclut l'ID et la configuration "from_attributes".
class PatientResponse(PatientCreate):
    id: int # <--- L'ID est inclus dans la réponse
    
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

#Obtenir un Patient
@app.get("/Patients/{patient_id}", response_model=PatientResponse)
def get_patient_by_id(patient_id:int, db:Session = Depends(get_db)):
    patient = db.query(patient_model).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient Not Found")
    return patient

@app.get("/patients/", response_model=List[PatientResponse])
def get_all_patients(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    patients=db.query(patient_model).offset(skip).limit(limit).all()
    return patients

@app.post("/patients/", response_model=PatientCreate)
def add_patient(patient:PatientCreate, db:Session = Depends(get_db)):
    try:
        db_patient = db.query(patient_model).filter(patient_model.name == patient.name).first()
        if db_patient :
            raise HTTPException(status_code=409, detail="Patient already exists")
        new_patient = patient_model(**patient.model_dump())
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
        return new_patient  
    except Exception as e:
        # Si quoi que ce soit échoue (l'erreur 500) :
        
        # 1. On l'affiche en grand dans le terminal
        print(f"!!! ERREUR LORS DE L'AJOUT DU PATIENT: {e} !!!")
        
        # 2. On annule la transaction
        db.rollback() 
        
        # 3. On renvoie l'erreur 500 au navigateur, 
        #    MAIS cette fois avec le message d'erreur !
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")
 

#Update user
"""@app.put("/user/{user_id}", response_model=UserResponse)
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

