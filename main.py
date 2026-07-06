from fastapi import FastAPI

from inventory_management.config import get_settings
from inventory_management.database import Base, engine
from inventory_management.models import Customer, Order, OrderItem, Product
from inventory_management.routers import customers, orders, products


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="Production-style Inventory and Order Management backend using FastAPI and MySQL.",
    )

    app.include_router(products.router)
    app.include_router(customers.router)
    app.include_router(orders.router)

    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "ok"}

    return app


Base.metadata.create_all(bind=engine)
app = create_app()

# Keep model imports referenced for metadata discovery in static analyzers.
_models = (Customer, Order, OrderItem, Product)
