from fastapi import FastAPI
from config.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from rotas import categoria, centro_treinamento, atleta

app = FastAPI(title="Workout API")

async def init_models():
    
    from models import categoria, centro_treinamento, atleta
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await init_models()

app.include_router(categoria.router)
app.include_router(centro_treinamento.router)
app.include_router(atleta.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

