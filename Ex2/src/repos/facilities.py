from repos.base import BaseRepository
from schemas.facilities import Facility
from src.models.facilities import FacilitiesOrm


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility
