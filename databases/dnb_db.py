from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

import config

dnb_engine = create_engine(
    url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
        config.AMEX_DB_USERNAME,
        config.DNB_DB_PASSWORD,
        config.DNB_DB_HOST,
        config.DNB_DB_PORT,
        config.DNB_DB_NAME,
    ),
)

dnb_base = automap_base()
dnb_base.prepare(dnb_engine, reflect=True)