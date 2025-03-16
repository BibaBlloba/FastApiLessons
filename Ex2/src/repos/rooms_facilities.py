from sqlalchemy import delete, insert, select

from src.models.facilities import RoomsFacilitiesOrm
from src.repos.base import BaseRepository


class Rooms_Facilities(BaseRepository):
    model = RoomsFacilitiesOrm

    async def set_facilities(self, room_id: int, facilities_ids: list[int]):
        get_current_facilities = select(self.model.facility_id).filter_by(
            room_id=room_id
        )
        result = await self.session.execute(get_current_facilities)
        current_facilities_ids: list[int] = result.scalars().all()
        ids_to_delete: list[int] = list(
            set(current_facilities_ids) - set(facilities_ids)
        )
        ids_to_create: list[int] = list(
            set(facilities_ids) - set(current_facilities_ids)
        )
        print(f"current: {facilities_ids}")
        print(f"to_delete: {ids_to_delete}")
        print(f"to_create: {ids_to_create}")

        if ids_to_delete:
            delete_stmt = delete(self.model).filter(
                self.model.room_id == room_id, self.model.facility_id.in_(ids_to_delete)
            )
            await self.session.execute(delete_stmt)

        if ids_to_create:
            create_stmt = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_create]
            )
            await self.session.execute(create_stmt)
