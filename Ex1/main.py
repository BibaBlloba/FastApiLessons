import uvicorn
from fastapi import Body, FastAPI, Query

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Berlin", "name": "berlin"},
]


# GET
@app.get(
    "/hotels",
    summary="Получение отелей",
    description="<h1>Развернутое описание</h1>",
)
async def get_hotels(
    id: int | None = Query(default=None),
    title: str | None = Query(default=None),
):
    if id == None and title == None:
        return hotels
    return [hotel for hotel in hotels if hotel["title"] == title or hotel["id"] == id]


# POST
@app.post("/hotels")
async def create_hotel(
    title: str = Body(),
    name: str = Body(),
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": title,
            "name": name,
        }
    )
    return {"status": "ok"}


# PUT
@app.put("/hotel/{hotel_id}")
async def put_hotel(
    hotel_id: int,
    title: str = Body(),
    name: str = Body(),
):
    global hotels
    hotels[hotel_id - 1]["title"] = title
    hotels[hotel_id - 1]["name"] = name
    return {"status": "ok"}


# PATCH
@app.patch("/hotel/{hotel_id}")
async def patch_hotel(
    hotel_id: int,
    title: str | None = Body(None),
    name: str | None = Body(None),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title is not None:
        hotel["title"] = title
    if name is not None:
        hotel["name"] = name
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
