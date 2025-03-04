from repos.base import BaseRepository
from repos.mappers.base import DataMapper
from repos.mappers.mappers import FacilitiesDataMapper
from schemas.facilities import Facility
from src.models.facilities import FacilitiesOrm


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper: DataMapper = FacilitiesDataMapper
