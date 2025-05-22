from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func, and_
from db.base import database
from db.tables import scan_jobs, repos, commits, findings

router = APIRouter()

class StatusResponse(BaseModel):
    scan_id: int
    status: str
    scanned_commits: int
    total_commits: int
    findings: int

@router.get("/{scan_id}", response_model=StatusResponse)
async def get_scan_status(scan_id: int):
    # Fetch the scan job by scan_id
    scan_job_query = select(scan_jobs).where(scan_jobs.c.id == scan_id)
    scan_job = await database.fetch_one(scan_job_query)
    if not scan_job:
        raise HTTPException(status_code=404, detail="Scan job not found")

    repo_id = scan_job["repo_id"]

    # Count scanned commits linked to this repo
    scanned_commits_query = select(func.count()).select_from(commits).where(
        and_(commits.c.repo_id == repo_id, commits.c.scanned == True)
    )
    scanned_commits = await database.fetch_val(scanned_commits_query) or 0

    # Count total commits linked to this repo
    total_commits_query = select(func.count()).select_from(commits).where(commits.c.repo_id == repo_id)
    total_commits = await database.fetch_val(total_commits_query) or 0

    # Count findings related to this repo via commits
    findings_query = (
        select(func.count())
        .select_from(findings.join(commits, findings.c.commit_id == commits.c.id))
        .where(commits.c.repo_id == repo_id)
    )
    findings_count = await database.fetch_val(findings_query) or 0

    # Use status field from the scan job itself
    status = scan_job["status"]

    return StatusResponse(
        scan_id=scan_id,
        status=status,
        scanned_commits=scanned_commits,
        total_commits=total_commits,
        findings=findings_count,
    )