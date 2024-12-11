from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRltns


class PackageDataMapper(DataMapper):
    db_model = PackageOrm
    schema = Package


class TypeDataMapper(DataMapper):
    db_model = TypeOrm
    schema = Type
