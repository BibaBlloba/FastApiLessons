from services.base import BaseService
from tasks.tasks import test_task


class FacilityService(BaseService):
    async def create_facility(self, data):
        result = await self.db.facilities.add(data)
        await self.db.commit()

        test_task.delay()
        return result
