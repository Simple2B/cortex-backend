import uvicorn

from app.setup import create_app
from app import models
from app.database import engine


app = create_app()

# models.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
