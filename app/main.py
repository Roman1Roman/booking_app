from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.appl import router
from app.bookings.router import router as bookings_router
from app.users.router import router as users_router
from app.hotels.router import router as hotels_router
from app.pages.router import router as pages_router
from app.images.router import router as images_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(users_router)
app.include_router(router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(pages_router)
app.include_router(images_router)

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Set-Cookie",
                   "Access-Control-Allow-Origin", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Methods"],
)