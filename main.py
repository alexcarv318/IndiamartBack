import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import indiamart, nextdoor, buildzoom # amex


@asynccontextmanager
async def lifespan(app: FastAPI):
    from databases.buildzoom_db import buildzoom_engine
    from databases.indiamart_db import indiamart_engine
    from databases.nextdoor_db import nextdoor_engine

    indiamart_connection = indiamart_engine.connect()
    nextdoor_connection = nextdoor_engine.connect()
    buildzoom_connection = buildzoom_engine.connect()
    # amex_engine.connect()

    yield

    indiamart_connection.close()
    nextdoor_connection.close()
    buildzoom_connection.close()
    # amex_engine.disconnect()

app = FastAPI(root_path="/api", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(indiamart.router)
app.include_router(nextdoor.router)
app.include_router(buildzoom.router)
#app.include_router(amex.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
