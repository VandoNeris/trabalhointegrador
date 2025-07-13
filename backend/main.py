from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
# from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import (
    usuario, 
    pessoa, 
    produtos, 
    maquina, 
    compra, 
    ordemservico, 
    servico, 
    compatibilidade, 
    consumocompra, 
    consumoservico, 
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Tratamento de exceções global
# @app.exception_handler(SQLAlchemyError)
# async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
#     return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Erro no banco de dados"})

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)})

### Incluindo as rotas da aplicação
app.include_router(usuario.router, tags=["Usuario"])
app.include_router(pessoa.router, tags=["Pessoa"])
app.include_router(produtos.router, tags=["Produtos"])
app.include_router(maquina.router, tags=["Maquina"])
app.include_router(compra.router, tags=["Compra"])
app.include_router(ordemservico.router, tags=["OrdemServico"])
app.include_router(servico.router, tags=["Servico"])
app.include_router(compatibilidade.router, tags=["Compatibilidade"])
app.include_router(consumocompra.router, tags=["ConsumoCompra"])
app.include_router(consumoservico.router, tags=["ConsumoServico"])
