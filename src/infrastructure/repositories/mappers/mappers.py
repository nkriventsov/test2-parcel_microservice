from src.domain.models.package import PackageOrm
from src.domain.models.package_type import PackageTypeOrm
from src.infrastructure.repositories.mappers.base import DataMapper
from src.shared.schemas.package_schemas import PackageResponse
from src.shared.schemas.type_schemas import TypeResponse


class PackageDataMapper(DataMapper):
    db_model = PackageOrm
    schema = PackageResponse


class PackageTypeDataMapper(DataMapper):
    db_model = PackageTypeOrm
    schema = TypeResponse
