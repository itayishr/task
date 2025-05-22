from fastapi import APIRouter, status
from pydantic import BaseModel, HttpUrl
from db.crud import get_repo_by_url, create_repo, create_scan_job
from task_queue.publisher import publish_scan_job

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

    # Publish scan job message to RabbitMQ task_queue
    publish_scan_job(
        scan_id=scan_id,
        repo_url=str(scan_req.repo_url),
        github_pat=scan_req.github_pat,
    )

    return ScanResponse(message="Scan job accepted", scan_id=scan_id)
