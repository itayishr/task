from fastapi import APIRouter, status
from pydantic import BaseModel, HttpUrl

router = APIRouter()

class ScanRequest(BaseModel):
    repo_url: HttpUrl
    github_pat: str

class ScanResponse(BaseModel):
    message: str

@router.post("/", response_model=ScanResponse, status_code=status.HTTP_202_ACCEPTED)
async def trigger_scan(scan_req: ScanRequest):
    return ScanResponse(message=f"Scan triggered for repo {scan_req.repo_url}")