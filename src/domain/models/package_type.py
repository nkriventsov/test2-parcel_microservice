from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.infrastructure.db.database import Base


class PackageType(Base):
    __tablename__ = "package_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    packages = relationship("Package", back_populates="package_type")
