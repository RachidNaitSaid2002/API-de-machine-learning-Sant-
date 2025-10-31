from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import joblib
import pandas as pd


app = FastAPI(title="Cardio Risk Prediction")

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
    
class PatientGet(BaseModel):
    age : int
    gender : int
    pressurehight : float
    pressurelow : float
    glucose : float
    kcm : float
    troponin : float
    impluse : float
    
class PredictionStatus(BaseModel):
    Status: str
    
    

class Config:
    from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get_db()

@app.get('/')
def read_root():
    return {"message" : "bienvenue sur mon API"}

@app.get("/patients/", response_model=list[PatientResponse])
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


@app.get('/patients/Pred_risk/{P_id}', response_model=PredictionStatus)
def Prediction_get(P_id: int, db: Session = Depends(get_db)):
    db_Patient = db.query(patient_model).filter(patient_model.id == P_id).first()
    
    if not db_Patient:
        raise HTTPException(status_code=404, detail="Not Found Patient")
    
    DF = pd.DataFrame([db_Patient.__dict__])
    expected_features = ['age', 'gender', 'pressurehight', 'pressurelow', 'glucose','kcm','troponin','impluse']  
    DF = DF[expected_features]
    print(DF)

    loaded_model = joblib.load("Model/joblib.dump")
    Prediction = loaded_model.predict(DF)[0]
    print(Prediction)
    
    if Prediction == 1:
        return {"Status" : "positive"}
    else :
        return {"Status" : "Negative"}
