from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import datetime as dt

from backend.app.core.security import create_access_token, verify_password
from backend.app.core.config import settings
from backend.database import get_session
from backend.app.schemas.usuario import Usuario, Token
from backend.app.schemas.MensagemResposta import MensagemResposta
from backend.app.crud import usuario as usuario_crud

router = APIRouter()

# Definindo excessão personalidada
http_exc_unauthn = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos", headers={"WWW-Authenticate": "Bearer"})

# Define que o token deve ser buscado na URL /usuario/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuario/token")

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[ OAuth2PasswordRequestForm, Depends() ], session: AsyncSession = Depends(get_session)) -> Token:
    
    usuario = await usuario_crud.buscar_usuario(session=session, nome_filter=form_data.username)
    if not usuario or not verify_password(form_data.password, usuario.senha):
        raise http_exc_unauthn

    access_token_expires = dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.nome, "tipo": usuario.tipo},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")

@router.post("/usuario", response_model=MensagemResposta, status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: Usuario, session: AsyncSession = Depends(get_session)):
    result = await usuario_crud.criar_usuario(session, usuario)

    return MensagemResposta(message="Usuario criada", id=result)
