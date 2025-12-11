from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

# Завантажуємо змінні середовища з .env файлу
load_dotenv()

app = FastAPI()

# Налаштування CORS для дозволу запитів з фронтенду
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # У продакшені слід обмежити конкретні домени
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def mask_secret(secret: str) -> str:
    """
    Маскує секрет, показуючи лише початок і кінець.
    Формат: Begin****End
    """
    if not secret:
        return "****"
    
    secret_len = len(secret)
    if secret_len <= 8:
        # Якщо секрет короткий, показуємо лише зірочки
        return "****"
    elif secret_len <= 12:
        # Для середніх секретів: перші 4 символи + зірочки
        return f"{secret[:4]}****"
    else:
        # Для довгих секретів: перші 4 символи + зірочки + останні 3 символи
        return f"{secret[:4]}****{secret[-3:]}"


@app.get("/api/info")
async def get_info():
    """
    Ендпоінт, який повертає інформацію з маскованим секретом.
    """
    # Читаємо секрет з .env файлу
    secret = os.getenv("SECRET_KEY", "")
    
    # Маскуємо секрет
    secret_preview = mask_secret(secret)
    
    return JSONResponse(content={
        "message": "Інформація успішно отримана",
        "secret_preview": secret_preview,
        "status": "success"
    })


@app.get("/")
async def root():
    """
    Кореневий ендпоінт для перевірки роботи сервера.
    """
    return {"message": "FastAPI сервер працює"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

