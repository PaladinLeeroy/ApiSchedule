from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.api.database import get_db

router = APIRouter()

@router.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    try:
        # Проверяем подключение к базе данных
        db = next(get_db())
        db.execute("SELECT 1")
        db.close()
        
        return {
            "status": "healthy",
            "message": "Приложение работает корректно",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Сервис недоступен: {str(e)}"
        ) 