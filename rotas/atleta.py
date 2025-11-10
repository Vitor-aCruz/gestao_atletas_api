from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.pagination import pagination_params
from schemas.atleta import AtletaIn, AtletaOut
from models.atleta import AtletaModel
from models.categoria import CategoriaModel
from models.centro_treinamento import CentroTreinamentoModel
from config.database import get_async_db

router = APIRouter(prefix="/atletas", tags=["Atletas"])

@router.post("/", response_model=AtletaOut, status_code=status.HTTP_201_CREATED)
async def create_atleta(atleta: AtletaIn, db: AsyncSession = Depends(get_async_db)):
    
    categoria_nome = atleta.categoria.nome
    centro_treinamento_nome = atleta.centro_treinamento.nome

    # Busca categoria pelo nome
    categoria = (
        await db.execute(select(CategoriaModel).filter_by(nome=categoria_nome))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A categoria '{categoria_nome}' não foi encontrada."
        )

    # Busca centro de treinamento pelo nome
    centro_treinamento = (
        await db.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
    ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O centro de treinamento '{centro_treinamento_nome}' não foi encontrado."
        )

    # Cria o novo atleta
    new_atleta = AtletaModel(
        nome=atleta.nome,
        cpf=atleta.cpf,
        idade=atleta.idade,
        peso=atleta.peso,
        altura=atleta.altura,
        sexo=atleta.sexo,
        categoria_id=categoria.pk_id,
        centro_treinamento_id=centro_treinamento.id,
        created_at=datetime.utcnow()
    )

    db.add(new_atleta)
    await db.commit()
    await db.refresh(new_atleta)

    
    return AtletaOut(
        pk_id=new_atleta.pk_id,
        nome=new_atleta.nome,
        cpf=new_atleta.cpf,
        idade=new_atleta.idade,
        peso=new_atleta.peso,
        altura=new_atleta.altura,
        sexo=new_atleta.sexo,
        categoria=atleta.categoria,
        centro_treinamento=atleta.centro_treinamento,
        created_at=new_atleta.created_at
    )

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

@router.get("/{atleta_id}", response_model=AtletaOut)
async def get_atleta(atleta_id: int, session: AsyncSession = Depends(get_async_db)):
    result = await session.execute(
        select(AtletaModel)
        .options(
            selectinload(AtletaModel.categoria),
            selectinload(AtletaModel.centro_treinamento)
        )
        .filter(AtletaModel.pk_id == atleta_id)
    )
    
    
    atleta = result.scalars().first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    
    return atleta

@router.get("/", response_model=list[AtletaOut])
async def list_atletas(db: AsyncSession = Depends(get_async_db), pagination: dict = Depends(pagination_params)):
    query = select(AtletaModel).limit(pagination["limit"]).offset(pagination["offset"])
    
    result = await db.execute(query)
    atletas = result.scalars().all()
    return [AtletaOut.model_validate(atleta) for atleta in atletas]

@router.patch("/atletas/{atleta_id}", response_model=AtletaOut)
async def update_atleta(atleta_id: int, atleta_update: AtletaIn, session: AsyncSession = Depends(get_async_db)):
    result = await session.execute(select(AtletaModel).filter(AtletaModel.pk_id == atleta_id))
    atleta = result.scalars().first()

    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")

    data = atleta_update.model_dump(exclude_unset=True)

    if "categoria" in data:
        categoria_info = data["categoria"]

    
    if "pk_id" in categoria_info:
        filtro = CategoriaModel.pk_id == categoria_info["pk_id"]
    elif "id" in categoria_info:
        filtro = CategoriaModel.pk_id == categoria_info["id"]
    elif "nome" in categoria_info:
        filtro = CategoriaModel.nome == categoria_info["nome"]
    else:
        raise HTTPException(status_code=400, detail="Categoria inválida")

    result = await session.execute(select(CategoriaModel).filter(filtro))
    categoria = result.scalars().first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    atleta.categoria = categoria
    del data["categoria"]


    if "centro_treinamento" in data:
        ct_info = data["centro_treinamento"]

    if "id" in ct_info:
        filtro_ct = CentroTreinamentoModel.id == ct_info["id"]
    elif "nome" in ct_info:
        filtro_ct = CentroTreinamentoModel.nome == ct_info["nome"]
    else:
        raise HTTPException(status_code=400, detail="Centro de Treinamento inválido")

    result = await session.execute(select(CentroTreinamentoModel).filter(filtro_ct))
    ct = result.scalars().first()
    if not ct:
        raise HTTPException(status_code=404, detail="Centro de Treinamento não encontrado")
    atleta.centro_treinamento = ct
    del data["centro_treinamento"]

    # ⚙️ Atualiza os demais campos
    for key, value in data.items():
        setattr(atleta, key, value)

    await session.commit()
    await session.refresh(atleta)
    return atleta

@router.delete("/{atleta_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_atleta(atleta_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(AtletaModel).filter_by(pk_id=atleta_id))
    atleta = result.scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta com ID {atleta_id} não encontrado."
        )

    await db.delete(atleta)
    await db.commit()
    
    return {"message": "Atleta deletado com sucesso"}