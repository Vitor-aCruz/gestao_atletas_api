from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.database import Base
from models.atleta import AtletaModel

class CentroTreinamentoModel(Base):
    __tablename__ = "centro_treinamento"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    localizacao: Mapped[str] = mapped_column(String(200), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(100), nullable=False)
    atletas: Mapped[list[AtletaModel]] = relationship("AtletaModel", back_populates="centro_treinamento")
