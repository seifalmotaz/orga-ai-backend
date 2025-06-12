from tortoise import Tortoise
import os

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://db.sqlite3")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "default_connection": "default",
            "models": [
                "src.database.models",
                "aerich.models",
            ],
        },
    },
}


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    # and specify the app name "models"
    # which contains models from "src.database.models"
    await Tortoise.init(config=TORTOISE_ORM)
    # Generate the schema
    await Tortoise.generate_schemas()
