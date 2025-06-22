from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from app.api.auth import SECRET_KEY, ALGORITHM
from app.api.models import User
from app.api.database import SessionLocal

async def auth_middleware(request: Request, call_next):
    # Получаем токен из cookie
    token = request.cookies.get("access_token")
    is_authenticated = False
    current_user = None

    if token:
        try:
            # Декодируем токен
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username:
                # Получаем пользователя из базы данных
                db = SessionLocal()
                try:
                    user = db.query(User).filter(User.username == username).first()
                    if user:
                        is_authenticated = True
                        current_user = {
                            "username": user.username,
                            "role": user.role
                        }
                finally:
                    db.close()
        except JWTError:
            pass

    # Добавляем данные в request.state
    request.state.is_authenticated = is_authenticated
    request.state.current_user = current_user

    # Продолжаем обработку запроса
    response = await call_next(request)
    return response

def template_middleware(templates: Jinja2Templates):
    """Middleware для добавления данных авторизации в шаблоны"""
    original_template_response = templates.TemplateResponse

    def template_response_wrapper(*args, **kwargs):
        request = kwargs.get("request")
        if request:
            # Добавляем данные авторизации в контекст шаблона
            kwargs["is_authenticated"] = request.state.is_authenticated
            kwargs["current_user"] = request.state.current_user
        return original_template_response(*args, **kwargs)

    templates.TemplateResponse = template_response_wrapper
    return templates 