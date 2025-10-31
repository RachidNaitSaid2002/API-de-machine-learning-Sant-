from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np 

app = FastAPI(title="Cardio Risk API")

# --- DataBase Setup
engine = create_engine("sqlite:///./patients.db", connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class patient_model(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
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
    gender : float
    pressurehight : float
    pressurelow : float
    glucose : float
    kcm : float
    troponin : float
    impluse : float

#Specifique : que les donnees medicales Sans Nom
class PatientGet(BaseModel):
    age : int
    gender : float
    pressurehight : float
    pressurelow : float
    glucose : float
    kcm : float
    troponin : float
    impluse : float
    
#lire les donnees depuis DB --> API
class Config:
    from_attributes = True

#ex : cle d'une chambre à l'hotel
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get_db()

# --- endpoint à la racine : Home
@app.get('/')
def read_root():
    return {"message" : "bienvenue sur mon API"}

#lire l'onglet : Patients
@app.get("/patients/", response_model=list[PatientResponse])
#R.Model : - garde du corps ---> priver password et ID de la liste à envoyer 
#          - age == [Integer] , Name == [String]
#          - list : definir la forme de return comme Liste  
def get_patients(db:Session = Depends(get_db)):
    Patients = db.query(patient_model).all()
    return Patients


@app.post("/patients/", response_model=PatientResponse)
def add_patients(new_patient:PatientResponse, db: Session = Depends(get_db)):
    db_patient = patient_model(**new_patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.get('/patients/{P_id}', response_model=PatientResponse)
def get_patient(P_id : int,db:Session = Depends(get_db)):
    db_Patient = db.query(patient_model).filter(patient_model.id == P_id).first()
    if not db_Patient :
        raise HTTPException(status_code=404, detail="Not Found")
    return db_Patient


@app.get('/patients/Pred_risk/{P_id}',response_model=PatientGet)
def Prediction_get(P_id : int, db:Session = Depends(get_db)):
    db_Patient = db.query(patient_model).filter(patient_model.id == P_id).first()
    if not db_Patient :
        raise HTTPException(status_code=404, detail="Not Found Patient")   
    My_Model = joblib.load("Model/joblib.dump")
    Prediction = My_Model.predict(db_Patient)
    
    return Prediction