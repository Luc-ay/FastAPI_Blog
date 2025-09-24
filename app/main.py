from fastapi import FastAPI
from .routers import user_router
# import logging

# logging.basicConfig(level=logging.WARNING)
# logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)




app = FastAPI()


app.include_router(user_router.router)

