from fastapi import FastAPI
import uvicorn
from bootstrap import setup_app , lifespan

VERSION = "0.0.1"

FASTAPI_INITIAL_DATA = {
    "openapi_tags": [
        {
            "name": "Tasks",
            "description": "Operations with tasks.",
            "externalDocs": {
                "description": "Tasks external docs",
                "url": "https://example.com/tasks-docs",
            },
        }
    ],
    "title": "TODO App",
    "description": "Todo application built with FastAPI",
    "version": VERSION,
    "terms_of_service": "http://example.com/terms/",
    "contact": {
        "name": "erfan karimi",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    "license_info": {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    "swagger_ui_parameters": {"displayRequestDuration": True},
    "lifespan":lifespan
}


def create_app() -> FastAPI:
    app = FastAPI(**FASTAPI_INITIAL_DATA)
    setup_app(app)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
