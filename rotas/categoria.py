from fastapi import APIRouter, HTTPException, status, Depends
from config.pagination import pagination_params
from schemas.categoria import CategoriaIn, CategoriaOut
from models.categoria import CategoriaModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_async_db


router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.post("/", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
async def create_categoria(categoria: CategoriaIn, db :AsyncSession = Depends(get_async_db)):
    new_categoria = CategoriaModel(nome=categoria.nome)
    existing_categoria = await db.execute(select(CategoriaModel).where(CategoriaModel.nome == categoria.nome))
    if existing_categoria.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Essa categoria ja existe.")
    
    db.add(new_categoria)
    await db.commit()
    await db.refresh(new_categoria)
    return CategoriaOut(id=new_categoria.pk_id, nome=new_categoria.nome)

@router.get("/{categoria_id}", response_model=CategoriaOut)
async def get_categoria(categoria_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(CategoriaModel).where(CategoriaModel.pk_id == categoria_id))
    categoria = result.scalars().one_or_none()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria not found")
    return CategoriaOut(id=categoria.pk_id, nome=categoria.nome)

@router.get("/", response_model=list[CategoriaOut])
async def list_categorias(db: AsyncSession = Depends(get_async_db), pagination: dict = Depends(pagination_params)):
    result = await db.execute(select(CategoriaModel)
                              .limit(pagination["limit"])
                              .offset(pagination["offset"]))
    categorias = result.scalars().all()
    return [CategoriaOut(id=c.pk_id, nome=c.nome) for c in categorias]
