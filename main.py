from fastapi import FastAPI
from api import scan, status

app = FastAPI(title="Entro Task - AWS Leak Scanner")

app.include_router(scan.router, prefix="/scan", tags=["scan"])
app.include_router(status.router, prefix="/status", tags=["status"])