# app/routers/usuarios.py
from fastapi import APIRouter, Depends, HTTPException
from ..models import UsuarioLogin, UsuarioCadastro
from ..auth import get_usuario, gerar_hash, autenticar_usuario, criar_token, get_usuario_atual
from ..database import usuarios
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from ..viacep import buscar_cep

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.get("/test")
def test():
    return {"mensagem": "OK, tudo certo!"}

@router.post("/registro")
def registrar(usuariox: UsuarioCadastro, usuario=Depends(get_usuario_atual)):
    if get_usuario(usuariox.username):
        raise HTTPException(status_code=400, detail='Usuário já existe')
    hash_senha = gerar_hash(usuariox.password)
    
   
    try:
        dados_cep = buscar_cep(usuariox.cep)
        endereco = {
            "cep": usuariox.cep,
            "logradouro": dados_cep.get("logradouro", ""),
            "bairro": dados_cep.get("bairro", ""),
            "cidade": dados_cep.get("localidade", ""),
            "uf": dados_cep.get("uf", ""),
            "numero": usuariox.numero,
            "complemento": usuariox.complemento
        }
        

        usuarios.insert_one({
            "username": usuariox.username, 
            "password": hash_senha,
            "endereco": endereco
        })
        
        return {"mensagem": "Usuário registrado com sucesso!", "endereco": endereco} 
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar CEP: {str(e)}")

@router.post("/login")
def logar(usuario: UsuarioLogin):
    autenticado = autenticar_usuario(usuario.username, usuario.password)

    if not autenticado:
        raise HTTPException(status_code=400, detail='Usuário ou Senha Inválidos')

    access_token = criar_token(
        data={"sub":autenticado["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"token": access_token, "expires": timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)} 