from fastapi import FastAPI

from routes.admin import router as admin_router
from routes.customer import router as customer_router


app = FastAPI(
    title="Admin and Customer API",
    version="1.0.0"
)


# Register routers
app.include_router(admin_router)
app.include_router(customer_router)