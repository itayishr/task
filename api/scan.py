from fastapi import APIRouter, Depends, status
from auth.dependencies import verify_token
from models.repo import ScanRequest, ScanResponse

router = APIRouter()

@router.post("/", response_model=ScanResponse, status_code=status.HTTP_202_ACCEPTED)
async def trigger_scan(
    scan_req: ScanRequest,
    token: str = Depends(verify_token),
):
    return ScanResponse(message="Scan job accepted", repo_id=1)