#Initializes the database params on initial load
from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, REAL

class DBConnect(Base):
    """
    Canary Sensor Data
    """
    __tablename__ = 'Canary Sensor Data'
    id = Column(DOUBLE_PRECISION, primary_key=True)
    device_uuid = Column(String(256))
    Sensor_Type = Column(String(256))
    Sensor_Value = Column(REAL)
    Sensor_Reading_Time = Column(Integer)
