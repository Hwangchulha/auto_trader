
from app.db import Base, engine
Base.metadata.create_all(bind=engine)
from app.services.scheduler import run_loop
if __name__ == "__main__":
    run_loop()
