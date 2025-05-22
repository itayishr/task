from typing import List, Optional
from sqlalchemy import select, insert, update
from db.base import database
from db.tables import repos, commits, findings, scan_jobs
from datetime import datetime


# --- Repos CRUD ---

async def create_repo(url: str) -> int:
    query = insert(repos).values(url=url)
    repo_id = await database.execute(query)
    return repo_id


async def get_repo_by_url(url: str) -> Optional[dict]:
    query = select(repos).where(repos.c.url == url)
    return await database.fetch_one(query)


async def update_repo_last_scanned_sha(repo_id: int, sha: str):
    query = (
        update(repos)
        .where(repos.c.id == repo_id)
        .values(last_scanned_sha=sha)
    )
    await database.execute(query)


# --- Commits CRUD ---

async def create_commit(sha: str, repo_id: int, date: datetime, scanned: bool = False) -> int:
    query = insert(commits).values(sha=sha, repo_id=repo_id, date=date, scanned=scanned)
    commit_id = await database.execute(query)
    return commit_id


async def get_commit_by_sha(sha: str) -> Optional[dict]:
    query = select(commits).where(commits.c.sha == sha)
    return await database.fetch_one(query)


async def mark_commit_scanned(commit_id: int):
    query = update(commits).where(commits.c.id == commit_id).values(scanned=True)
    await database.execute(query)


# --- Findings CRUD ---

async def create_finding(
        commit_id: int,
        type_: str,
        masked_value: str,
        file_path: str,
        line_no: int
) -> int:
    query = insert(findings).values(
        commit_id=commit_id,
        type=type_,
        masked_value=masked_value,
        file_path=file_path,
        line_no=line_no,
    )
    finding_id = await database.execute(query)
    return finding_id


async def get_findings_by_commit(commit_id: int) -> List[dict]:
    query = select(findings).where(findings.c.commit_id == commit_id)
    return await database.fetch_all(query)


# --- Scan Jobs CRUD ---

async def create_scan_job(repo_id: int) -> int:
    query = insert(scan_jobs).values(repo_id=repo_id, status="pending")
    scan_id = await database.execute(query)
    return scan_id


async def get_scan_job_by_id(scan_id: int) -> Optional[dict]:
    query = select(scan_jobs).where(scan_jobs.c.id == scan_id)
    return await database.fetch_one(query)


async def update_scan_job_status(scan_id: int, status: str):
    query = (
        update(scan_jobs)
        .where(scan_jobs.c.id == scan_id)
        .values(status=status)
    )
    await database.execute(query)


from sqlalchemy import select, join
from db.tables import findings, commits, scan_jobs


async def get_scan_job_by_id(scan_id: int):
    query = select(scan_jobs).where(scan_jobs.c.id == scan_id)
    return await database.fetch_one(query)


async def get_findings_by_scan_id(scan_id: int):
    j = join(findings, commits, findings.c.commit_id == commits.c.id)
    j = join(j, scan_jobs, commits.c.repo_id == scan_jobs.c.repo_id)
    query = (
        select(
            findings.c.type,
            findings.c.masked_value,
            findings.c.file_path,
            findings.c.line_no,
            commits.c.sha.label("commit_sha"),
            commits.c.date.label("commit_date"),
        )
        .select_from(j)
        .where(scan_jobs.c.id == scan_id)
        .order_by(commits.c.date.desc())
    )
    return await database.fetch_all(query)
