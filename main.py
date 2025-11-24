from fastapi import FastAPI
from app.routers import auth_router, course_router

app = FastAPI(title="Course Management System")

app.include_router(auth_router.router)
app.include_router(course_router.router)
