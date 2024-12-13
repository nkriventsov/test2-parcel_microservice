from src.domain.models import PackageTypeOrm
from src.infrastructure.repositories.base import BaseRepository
from src.infrastructure.repositories.mappers import PackageTypeDataMapper


class TypeRepository(BaseRepository):
    model = PackageTypeOrm
    mapper = PackageTypeDataMapper
