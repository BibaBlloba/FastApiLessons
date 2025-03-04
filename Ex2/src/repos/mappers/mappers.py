from repos.mappers.base import DataMapper
from schemas.facilities import Facility
from schemas.hotels import Hotel
from schemas.rooms import Room
from schemas.users import User
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class UsersDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility
