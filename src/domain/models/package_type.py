from sqlalchemy.orm import Mapped, mapped_column, relationship  # Импорт классов и функций для работы с ORM SQLAlchemy
from src.infrastructure.db.database import Base  # Импорт базового класса модели из модуля базы данных


# Определение модели для таблицы "package_types"
class PackageTypeOrm(Base):
    __tablename__ = "package_types"  # Имя таблицы в базе данных

    # Колонка для идентификатора с первичным ключом и индексом для оптимизации поиска
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Колонка для имени типа пакета, обязательное поле, уникальное значение
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    # Связь "один ко многим" с таблицей "packages", устанавливается через поле package_type в модели "Package"
    packages: Mapped[list["PackageOrm"]] = relationship("PackageOrm", back_populates="package_type")
