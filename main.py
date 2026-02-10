import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import create , search , delete, update, ai_history, users
from contextlib import asynccontextmanager
from database import init_db

@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield

app = FastAPI(
    title = "Task Pilot DB Service",
    version = "1.0",
    lifespan=lifespan,
    docs_url = "/swagger",
    servers = [{
        "url" : "http://localhost:5014",
        "description" : "Local Development Server"
    }],
    swagger_ui_parameters = {"defaultModelsExpandDepth" : -1}

)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = ["*"],
#     allow_methods = ["GET","POST","PUT","DELETE"],
#     allow_headers = ["Authorization","Content-Type"]
# )


app.include_router(create.router)
app.include_router(search.router)
app.include_router(update.router)
app.include_router(delete.router)
app.include_router(ai_history.router)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=5014)