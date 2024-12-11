from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.db.database import Base


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    type_id = Column(Integer, ForeignKey("package_types.id"), nullable=False)
    content_value = Column(Float, nullable=False)

    package_type = relationship("PackageType", back_populates="packages")
