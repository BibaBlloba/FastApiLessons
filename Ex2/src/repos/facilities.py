from models.facilities import FacilitiesOrm
from repos.base import BaseRepository
from schemas.facilities import Facility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility
