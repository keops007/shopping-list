import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()
logging.basicConfig(level=logging.INFO)

os.makedirs("./uploads", exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    import config.database as db
    import models.user          # inregistreaza modelele cu Base
    import models.shopping_item

    db.connect_db()
    db.Base.metadata.create_all(bind=db.engine)
    yield


app = FastAPI(title="ShopList API", lifespan=lifespan)

# Fisiere statice
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Pagini HTML
@app.get("/", include_in_schema=False)
def index(): return FileResponse("static/index.html")

@app.get("/register", include_in_schema=False)
def register_page(): return FileResponse("static/register.html")

@app.get("/login", include_in_schema=False)
def login_page(): return FileResponse("static/login.html")

@app.get("/profile", include_in_schema=False)
def profile_page(): return FileResponse("static/profile.html")

@app.get("/shopping", include_in_schema=False)
def shopping_page(): return FileResponse("static/shopping.html")

@app.get("/logo.png", include_in_schema=False)
def logo(): return FileResponse("logo.png")

# Rute API
from handlers import auth_handler, profile_handler, shopping_handler

app.include_router(auth_handler.router)
app.include_router(profile_handler.router, prefix="/api")
app.include_router(shopping_handler.router, prefix="/api")
