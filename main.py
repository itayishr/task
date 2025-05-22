from fastapi import FastAPI
from api import scan, status
from db.base import database, metadata, engine
from api import ui


app = FastAPI(title="Entro Task - AWS Leak Scanner")

app.include_router(ui.router, prefix="/ui")
app.include_router(scan.router, prefix="/scan", tags=["scan"])
app.include_router(status.router, prefix="/status", tags=["status"])

metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
