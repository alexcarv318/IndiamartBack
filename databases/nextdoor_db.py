from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

import config

nextdoor_engine = create_engine(
    url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
        config.AMEX_DB_USERNAME,
        config.NEXTDOOR_DB_PASSWORD,
        config.NEXTDOOR_DB_HOST,
        config.NEXTDOOR_DB_PORT,
        config.NEXTDOOR_DB_NAME,
    ),
)

nextdoor_base = automap_base()
nextdoor_base.prepare(nextdoor_engine, reflect=True)