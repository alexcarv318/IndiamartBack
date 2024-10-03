from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

import config

engine = create_engine(
    url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
        config.DB_USERNAME,
        config.DB_PASSWORD,
        config.DB_HOST,
        config.DB_PORT,
        config.DB_NAME,
    ),
)

Base = automap_base()
Base.prepare(engine, reflect=True)
