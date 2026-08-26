from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.admin import router as admin_router
from routes.customer import router as customer_router
from routes.account import router as account_router


app = FastAPI(
    title="Digital Bank API",
    version="2.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Digital Bank API is running"
    }


app.include_router(admin_router)
app.include_router(customer_router)
app.include_router(account_router)