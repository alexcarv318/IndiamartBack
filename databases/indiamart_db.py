from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

import config

indiamart_engine = create_engine(
    url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
        config.INDIAMART_DB_USERNAME,
        config.INDIAMART_DB_PASSWORD,
        config.INDIAMART_DB_HOST,
        config.INDIAMART_DB_PORT,
        config.INDIAMART_DB_NAME,
    ),
)

indiamart_base = automap_base()
indiamart_base.prepare(indiamart_engine, reflect=True)