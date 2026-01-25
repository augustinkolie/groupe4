import random
from datetime import datetime
from typing import List
from ingestion.adapters.base import BaseAdapter, UnifiedPayload, UnifiedLocation, UnifiedMeasurement

class MockSensorAdapter(BaseAdapter):
    """
    Simulates data from a physical sensor for testing purposes.
    """
    
    def fetch_data(self) -> List[UnifiedPayload]:
        # Simulate data for Labé
        payload = UnifiedPayload(
            location=UnifiedLocation(
                lat=11.318,
                lon=-12.283,
                name="Labé Mock Station",
                region="Moyenne Guinée"
            ),
            measurements=UnifiedMeasurement(
                pm25=random.uniform(10, 50),
                pm10=random.uniform(20, 80),
                co=random.uniform(0.1, 1.5),
                humidity=random.uniform(30, 70),
                temperature=random.uniform(20, 35)
            ),
            source_type="SENSOR",
            source_id="mock_labe_01",
            captured_at=datetime.now()
        )
        return [payload]
