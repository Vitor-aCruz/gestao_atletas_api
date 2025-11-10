from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.database import Base



class AtletaModel(Base):
    __tablename__ = "atleta"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria.pk_id"), nullable=False)
    centro_treinamento_id: Mapped[int] = mapped_column(ForeignKey("centro_treinamento.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    categoria: Mapped["CategoriaModel"] = relationship("CategoriaModel", back_populates="atletas", lazy="selectin")
    centro_treinamento: Mapped["CentroTreinamentoModel"] = relationship("CentroTreinamentoModel", back_populates="atletas", lazy="selectin")