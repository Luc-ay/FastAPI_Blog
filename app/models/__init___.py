from ..core import database
from ..models import user_models

def init_db():
    user_models.Base.metadata.create_all(bind=database.engine)

if __name__ == "__main__":
    init_db()