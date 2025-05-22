from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

class StatusResponse(BaseModel):
    repo_id: int
    status: str
    scanned_commits: int
    findings: int

@router.get("/{repo_id}", response_model=StatusResponse)
async def get_scan_status(repo_id: int):
    # TODO: Replace with real DB lookup or logic
    dummy_status = StatusResponse(
        repo_id=repo_id,
        status="in_progress",
        scanned_commits=42,
        findings=3,
    )
    return dummy_status