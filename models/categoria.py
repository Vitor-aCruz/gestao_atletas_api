from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.database import Base


class CategoriaModel(Base):
    __tablename__ = "categoria"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50),unique=True, nullable=False)
    atletas: Mapped[list["AtletaModel"]] = relationship("AtletaModel", back_populates="categoria")