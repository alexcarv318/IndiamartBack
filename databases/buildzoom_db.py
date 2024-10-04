from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

import config

buildzoom_engine = create_engine(
    url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
        config.BUILDZOOM_DB_USERNAME,
        config.BUILDZOOM_DB_PASSWORD,
        config.BUILDZOOM_DB_HOST,
        config.BUILDZOOM_DB_PORT,
        config.BUILDZOOM_DB_NAME,
    ),
)

buildzoom_base = automap_base()
buildzoom_base.prepare(buildzoom_engine, reflect=True)