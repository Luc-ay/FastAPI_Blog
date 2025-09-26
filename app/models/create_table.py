from app.models import User, Task
from app.core.database import Base, engine

print("Tables to create:", Base.metadata.tables.keys())

def create_db_and_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
    print("Database and tables created.")