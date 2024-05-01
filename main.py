import uvicorn
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from routers.projects import router as project_router
from routers.profiles import router as profile_router
from routers.roles import router as role_router
from routers.users import router as user_router
from routers.events import router as event_router
from routers.sessions import router as session_router
from routers.AuthReg import router as authReg_router
from routers.firms import router as firm_router
from routers.timetable import router as timetable_router
from routers.TaskManagerBoard import router as taskManagerBoard
from routers.files import router as files

app = FastAPI()

app.mount("/Documents", StaticFiles(directory="Documents"), name="Documents")

# Добавляем middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Здесь можно указать список допустимых источников запросов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(
    router=project_router,
    prefix='/projects'
)
app.include_router(
    router=role_router,
    prefix='/roles'
)
app.include_router(
    router=profile_router,
    prefix='/profiles'
)
app.include_router(
    router=user_router,
    prefix='/users'
)
app.include_router(
    router=event_router,
    prefix='/events'
)
app.include_router(
    router=session_router,
    prefix='/session'
)
app.include_router(
    router=authReg_router,
    prefix='/authReg'
)
app.include_router(
    router=firm_router,
    prefix='/firms'
)
app.include_router(
    router=timetable_router,
    prefix='/timetable'
)
app.include_router(
    router=taskManagerBoard,
    prefix='/taskmanager'
)

app.include_router(
    router=files,
    prefix='/files'
)

# Пример пути к SSL ключу и сертификату
ssl_key_path = "/SSL/name.key"
ssl_cert_path = "/SSL/cert.key"