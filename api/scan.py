from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, HttpUrl
from db.crud import get_repo_by_url, create_repo, create_scan_job

router = APIRouter()


class ScanRequest(BaseModel):
    repo_url: HttpUrl
    github_pat: str


class ScanResponse(BaseModel):
    message: str
    scan_id: int


@router.post("/", response_model=ScanResponse, status_code=status.HTTP_202_ACCEPTED)
async def trigger_scan(scan_req: ScanRequest):
    existing_repo = await get_repo_by_url(str(scan_req.repo_url))
    if existing_repo:
        repo_id = existing_repo["id"]
    else:
        repo_id = await create_repo(str(scan_req.repo_url))

    scan_id = await create_scan_job(repo_id)

    # TODO: enqueue or start scanning job here

    return ScanResponse(message="Scan job accepted", scan_id=scan_id)
