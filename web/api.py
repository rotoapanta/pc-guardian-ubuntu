"""Optional FastAPI health service for PC Guardian Ubuntu."""

from fastapi import FastAPI

from core.version import __version__

app = FastAPI(title="PC Guardian Ubuntu", version=__version__)


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health and application version."""
    return {"status": "ok", "version": __version__}
