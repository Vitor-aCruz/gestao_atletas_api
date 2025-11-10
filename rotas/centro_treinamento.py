from fastapi import APIRouter, Depends, HTTPException, status
from config.pagination import pagination_params
from schemas.centro_treinamento import CentroTreinamentoIn, CentroTreinamentoOut
from models.centro_treinamento import CentroTreinamentoModel
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_async_db
from sqlalchemy.future import select

router = APIRouter(prefix="/centros_treinamento", tags=["Centros de Treinamento"])

@router.post("/", response_model=CentroTreinamentoOut, status_code=status.HTTP_201_CREATED)
async def create_centro_treinamento(centro: CentroTreinamentoIn, db=Depends(get_async_db)):
    new_centro = CentroTreinamentoModel(
        nome=centro.nome,
        localizacao=centro.localizacao,
        proprietario=centro.proprietario
    )
    existing_centro = await db.execute(select(CentroTreinamentoModel))
    if existing_centro.scalars().first():  
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Centro ja existe")
    
    db.add(new_centro)
    await db.commit()
    await db.refresh(new_centro)
    return CentroTreinamentoOut(
        id=new_centro.id,
        nome=new_centro.nome
    )
    
@router.get("/{centro_id}", response_model=CentroTreinamentoOut)
async def get_centro_treinamento(centro_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(CentroTreinamentoModel).where(CentroTreinamentoModel.id == centro_id))
    centro = result.scalars().one_or_none()
    if not centro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Centro de Treinamento not found")
    return CentroTreinamentoOut(
        id=centro.id,
        nome=centro.nome
    )
@router.get("/", response_model=list[CentroTreinamentoOut])
async def list_centros_treinamento(db=Depends(get_async_db), pagination: dict = Depends(pagination_params)):
    result = await db.execute(select(CentroTreinamentoModel)
                              .limit(pagination["limit"])
                              .offset(pagination["offset"]))
    centros = result.scalars().all()
    return [CentroTreinamentoOut(id=c.id, nome=c.nome) for c in centros]