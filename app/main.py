from fastapi import FastAPI, Request, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.database import init_db
from app.api.router import api_router, html_router
from app.api.health import router as health_router
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse, JSONResponse
from app.api.auth import get_current_user, get_current_active_user
from app.api.schemas import UserResponse
from app.api.database import get_db
from app.api.middleware import auth_middleware, template_middleware
from typing import Optional
import logging
import sys
import os

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app_URL = '127.0.0.1'

# Инициализация базы данных
init_db()

app = FastAPI(
    title="Schedule Management API",
    description="API для управления расписанием учебного заведения",
    version="1.0.0",
    debug=settings.DEBUG
)

# Добавляем middleware для авторизации
app.middleware("http")(auth_middleware)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Настраиваем шаблоны с middleware
templates = Jinja2Templates(directory="app/templates")
templates = template_middleware(templates)

# Подключаем роутеры
app.include_router(html_router)  # HTML маршруты без префикса
app.include_router(api_router)   # API маршруты с префиксом /api
app.include_router(health_router)  # Health check маршруты

# OAuth2 схема для защиты маршрутов
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token", auto_error=False)

async def get_current_user_optional(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Depends(oauth2_scheme),
    db = Depends(get_db)
):
    """Получение текущего пользователя (опционально)"""
    logger.info(f"Checking authorization. Header: {authorization}, Token: {token is not None}")
    
    # Проверяем токен из заголовка Authorization
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        logger.info("Using token from Authorization header")
    elif token is None:
        logger.info("No token provided")
        return None

    try:
        user = await get_current_user(token, db)
        logger.info(f"User authenticated: {user.username} ({user.role})")
        return UserResponse(
            id=user.id,
            username=user.username,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at
        )
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        return None

@app.get("/api/check-auth")
async def check_auth(current_user: Optional[UserResponse] = Depends(get_current_user_optional)):
    """Эндпоинт для проверки авторизации"""
    logger.info(f"Checking auth status. User: {current_user.username if current_user else None}")
    if current_user:
        return {"authenticated": True, "user": current_user}
    return {"authenticated": False}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Обработчик ошибок HTTP"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/unauthorized", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("error.html", {
        "request": request,
        "error_code": exc.status_code,
        "error_message": exc.detail,
        "is_authenticated": False,
        "current_user": None
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.HOST, 
        port=settings.PORT,
        log_level="info"
    )

# запуск: uvicorn app.main:app --reload


# todo
# Списки для преподавателей