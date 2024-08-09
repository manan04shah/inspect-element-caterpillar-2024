from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from typing import List, Optional
from datetime import datetime

client = MongoClient("mongodb+srv://a7x:a7x@inspect-element.dwg4o.mongodb.net/?retryWrites=true&w=majority&appName=inspect-element")
db = client["inspect-element"]  # Replace with your database name
collection = db["inspections"]  # Replace with your collection name

app = FastAPI()

class TireData(BaseModel):
    pressure_left_front: Optional[float] = None
    pressure_right_front: Optional[float] = None
    condition_left_front: str
    condition_right_front: str
    pressure_left_rear: Optional[float] = None
    pressure_right_rear: Optional[float] = None
    condition_left_rear: str
    condition_right_rear: str
    summary: Optional[str] = None
    images: List[str] = []

class BatteryData(BaseModel):
    make: str
    replacement_date: Optional[datetime] = None
    voltage: Optional[str] = None
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

class Inspection(BaseModel):
    truck_serial_number: str
    truck_model: str
    inspector_name: str
    employee_id: str
    date_time: datetime = Field(default_factory=datetime.utcnow)
    location: str
    geo_coordinates: Optional[str] = None
    service_meter_hours: int
    customer_name: str
    cat_customer_id: str
    tires: TireData
    battery: BatteryData
    exterior: ExteriorData
    brakes: BrakesData
    engine: EngineData
    voice_of_customer: VoiceOfCustomerData


@app.post("/inspections/")
async def add_inspection(inspection: Inspection):
    try:
        # Convert the inspection to a dictionary using model_dump and insert it into MongoDB
        inspection_dict = inspection.model_dump()
        result = collection.insert_one(inspection_dict)
        return {"message": "Inspection added successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
