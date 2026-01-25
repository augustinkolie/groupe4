from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class UnifiedLocation(BaseModel):
    lat: float
    lon: float
    name: str
    region: Optional[str] = None

class UnifiedMeasurement(BaseModel):
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    co: Optional[float] = None
    no2: Optional[float] = None
    so2: Optional[float] = None
    o3: Optional[float] = None
    humidity: Optional[float] = None
    temperature: Optional[float] = None

class UnifiedPayload(BaseModel):
    location: UnifiedLocation
    measurements: UnifiedMeasurement
    source_type: str = Field(..., pattern="^(API|SENSOR)$")
    source_id: str
    captured_at: datetime

class BaseAdapter(ABC):
    """
    Abstract base class for all data sources (OpenAQ, OpenWeather, Sensors).
    """
    
    @abstractmethod
    def fetch_data(self) -> List[UnifiedPayload]:
        """Fetch and normalize data into UnifiedPayload list."""
        pass
