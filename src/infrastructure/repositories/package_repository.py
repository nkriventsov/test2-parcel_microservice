from src.domain.models import PackageOrm
from src.infrastructure.repositories.base import BaseRepository
from src.infrastructure.repositories.mappers import PackageDataMapper


class PackageRepository(BaseRepository):
    model = PackageOrm
    mapper = PackageDataMapper
