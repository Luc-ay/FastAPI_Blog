from fastapi import FastAPI, Request
from .routers import user_router, task_router
from fastapi.responses import JSONResponse
from app.core.database import Base, engine
import app.models

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)



app = FastAPI()


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "details": str(exc),  # optional: include this for debugging
            # "trace": traceback.format_exc()  # optional: for full trace (not in production)
        },
    )


app.include_router(user_router.router)
app.include_router(task_router.router)

