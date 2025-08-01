from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from api.adapters.routes.flight_routes import flights_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flights_router)


@app.get("/health-check")
def health_check():
    return Response(
        content="OK", media_type="text/plain", status_code=status.HTTP_200_OK
    )
