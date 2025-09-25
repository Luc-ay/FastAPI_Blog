from app.models.task_models import Task
from app.models.user_models import User  # if you have user model
from app.core.database import Base, engine

print("Tables to create:", Base.metadata.tables.keys())

def create_db_and_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
    print("Database and tables created.")