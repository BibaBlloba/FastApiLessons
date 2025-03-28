from src.models.facilities import FacilitiesOrm
from src.repos.base import BaseRepository
from src.repos.mappers.base import DataMapper
from src.repos.mappers.mappers import FacilitiesDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper: DataMapper = FacilitiesDataMapper
