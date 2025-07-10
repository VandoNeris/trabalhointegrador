from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import (
    pessoa, 
    compra, 
    ordemservico
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tratamento de exceções global
# @app.exception_handler(SQLAlchemyError)
# async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
#     return JSONResponse(status_code=500, content={"detail": "Erro no banco de dados"})

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

### Incluindo as rotas da aplicação
app.include_router(pessoa.router, tags=["Pessoa"])
app.include_router(compra.router, tags=["Compra"])
app.include_router(ordemservico.router, tags=["OrdemServico"])
