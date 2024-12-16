from sqlalchemy import ForeignKey  # Импорт для создания внешних ключей
from sqlalchemy.orm import Mapped, mapped_column, relationship  # Импорт инструментов для работы с ORM
from src.infrastructure.db.database import Base  # Импорт базового класса модели


# Определение модели для таблицы "packages"
class PackageOrm(Base):
    __tablename__ = "packages"  # Имя таблицы в базе данных

    # Идентификатор пакета, первичный ключ, индексируется для быстрого поиска
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Имя пакета, обязательное поле
    name: Mapped[str] = mapped_column(nullable=False)

    # Вес пакета, обязательное поле
    weight: Mapped[float] = mapped_column(nullable=False)

    # Внешний ключ, ссылающийся на таблицу "package_types", обязательное поле
    type_id: Mapped[int] = mapped_column(ForeignKey("package_types.id"), nullable=False)

    # Стоимость содержимого пакета, обязательное поле
    content_value: Mapped[float] = mapped_column(nullable=False)

    session_id: Mapped[str] = mapped_column(nullable=False, index=True)

    # Поле стоимости доставки, которое может быть NULL
    delivery_cost: Mapped[float | None] = mapped_column(nullable=True)

    # Связь "многие к одному" с моделью "PackageType", обратная связь определяется в "PackageType"
    package_type: Mapped["PackageTypeOrm"] = relationship("PackageTypeOrm", back_populates="packages")

