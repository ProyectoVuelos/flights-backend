from uvicorn import run

from api.utils.env_manager import settings

if __name__ == "__main__":
    run(
        "api.index:app",
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        reload=True,
    )
