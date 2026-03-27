from pydantic import BaseModel
from typing import Optional


class ParsedReport(BaseModel):
    machine_id: str
    machine_type: Optional[str] = "unknown"
    temperature: str
    vibration: str
    noise: Optional[str] = "unknown"
    pressure: Optional[str] = "unknown"
    coolant: Optional[str] = "unknown"
    lubrication: Optional[str] = "unknown"
    last_service: str
    description: Optional[str] = ""
    observation: Optional[str] = ""
    warning: Optional[str] = ""
    issues: list[str] = []
    full_text: Optional[str] = ""
