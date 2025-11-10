"""Custom exception classes for the application"""
from fastapi import HTTPException, status

class DatabaseException(HTTPException):
    def __init__(self, detail: str = "Database error occurred"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class ModelNotTrainedException(HTTPException):
    def __init__(self, detail: str = "Model not trained yet"):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)

class InvalidDataException(HTTPException):
    def __init__(self, detail: str = "Invalid data provided"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class SensorNotFoundException(HTTPException):
    def __init__(self, sensor_id: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sensor '{sensor_id}' not found")