from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from presentation.controllers.user_controller import user_controller
from presentation.controllers.conversation_controller import conversation_controller
from infrastructure.config.db import init_models

app = FastAPI()

# Configuración CORS para todos los orígenes (incluye localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración CORS específica para neidercode.com (comentada)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://neidercode.com"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.include_router(user_controller.router)
app.include_router(conversation_controller.router)

@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.on_event("startup")
async def on_startup():
    await init_models() 