from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

import config

amex_engine = create_engine(
    url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
        config.AMEX_DB_USERNAME,
        config.AMEX_DB_PASSWORD,
        config.AMEX_DB_HOST,
        config.AMEX_DB_PORT,
        config.AMEX_DB_NAME,
    ),
)

amex_base = automap_base()
amex_base.prepare(amex_engine, reflect=True)