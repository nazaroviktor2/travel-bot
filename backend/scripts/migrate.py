import asyncio
import logging

from sqlalchemy.exc import IntegrityError
from webapp.db.postgres import engine
from webapp.models.meta import Base


async def main() -> None:
    try:
        async with engine.begin() as conn:
            logging.info("-----------------------gp-----------------------")

            await conn.run_sync(Base.metadata.create_all)
    except IntegrityError:
        logging.exception("Already exists")
    except Exception as err:
        logging.info(f"Materialized already exists: {err}")


if __name__ == "__main__":
    asyncio.run(main())
