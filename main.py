from fastapi import FastAPI

from src.backend.routers.product import router as router_product
from src.backend.routers.order import router as route_order

app = FastAPI(
    title="My_app"
)


@app.get("/")
async def welcome() -> dict:
    return {"message": "Wellcome API development for warehouse management"}


app.include_router(router_product)
app.include_router(route_order)
