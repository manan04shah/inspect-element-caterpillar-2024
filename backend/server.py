from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from typing import List, Optional
from datetime import datetime

import dotenv
from os import getenv

import gemini

dotenv.load_dotenv()
mongoURI = getenv("MONGO_URI")

client = MongoClient(mongoURI)
db = client["inspect-element"]  # Replace with your database name
collection = db["inspections"]  # Replace with your collection name

app = FastAPI()

class TireData(BaseModel):
    pressure_left_front: float = None
    pressure_right_front: float = None
    condition_left_front: str
    condition_right_front: str
    pressure_left_rear: float = None
    pressure_right_rear: float = None
    condition_left_rear: str
    condition_right_rear: str
    summary: Optional[str] = None
    images: List[str] = []

class BatteryData(BaseModel):
    make: str
    replacement_date: datetime
    voltage: str
    water_level: str
    damage: bool
    leak_or_rust: bool
    summary: Optional[str] = None
    images: List[str] = []

class ExteriorData(BaseModel):
    rust_or_damage: bool
    oil_leak_in_suspension: bool
    summary: Optional[str] = None
    images: List[str] = []

class BrakesData(BaseModel):
    fluid_level: str
    condition_front: str
    condition_rear: str
    emergency_brake: str
    summary: Optional[str] = None
    images: List[str] = []

class EngineData(BaseModel):
    rust_or_damage: bool
    oil_condition: str
    oil_color: str
    fluid_condition: str
    fluid_color: str
    oil_leak: bool
    summary: Optional[str] = None
    images: List[str] = []

class VoiceOfCustomerData(BaseModel):
    feedback: Optional[str] = None
    images: List[str] = []
    
class CustomChecklist(BaseModel):
    name: str
    value: str
    is_required: bool

class CustomChecklistData(BaseModel):
    checklist: List[CustomChecklist]
    summary: Optional[str] = None
    images: List[str] = []

class Inspection(BaseModel):
    vehicle_serial_number: str
    vehicle_model: str
    inspector_name: str
    employee_id: str
    date_time: datetime = Field(default_factory=datetime.utcnow)
    location: str
    geo_coordinates: Optional[str] = None
    service_meter_hours: int
    customer_name: str
    cat_customer_id: str
    tires: Optional[TireData] = None
    battery: Optional[BatteryData] = None
    exterior: Optional[ExteriorData] = None
    brakes: Optional[BrakesData] = None
    engine: Optional[EngineData] = None
    custom_checklist: Optional[CustomChecklistData] = None
    voice_of_customer: Optional[VoiceOfCustomerData] = None  


@app.post("/inspections/")
async def add_inspection(inspection: Inspection):
    try:
        # Convert the inspection to a dictionary using model_dump and insert it into MongoDB
        inspection_dict = inspection.model_dump()
        result = collection.insert_one(inspection_dict)
        return {"message": "Inspection added successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/gemini/custom")
async def gemini_custom_prompt(prompt: str):
    try:
        response = gemini.gemini_custom_prompt(prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/gemini/inspect-tyres")
async def inspect_tyres(tire_data: TireData, equipment_type: str):
    try:
        response = gemini.inspect_tyres(tire_data.model_dump(), equipment_type=equipment_type)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))