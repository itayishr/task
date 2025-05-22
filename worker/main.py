import logging
from datetime import datetime

from db.base import database
from db.crud import (
    create_commit,
    mark_commit_scanned,
    create_finding,
    update_scan_job_status,
    get_commit_by_sha,
    get_repo_by_url,
)
from worker.github_api import (
    get_commits,
    get_commit_detail,
    parse_github_repo_url,
    get_default_branch,
)
from worker.secret_scanner import scan_text_for_secrets


def mask_secret(secret: str) -> str:
    if len(secret) <= 8:
        return secret
    return f"{secret[:4]}{'*' * (len(secret) - 8)}{secret[-4:]}"


async def run_scan(scan_id: int, repo_url: str, github_pat: str):
    await database.connect()
    try:
        repo = await get_repo_by_url(repo_url)
        if not repo:
            logging.error(f"Repo not found for URL {repo_url}")
            await update_scan_job_status(scan_id, "failed")
            return
        repo_id = repo["id"]

        owner, repo_name = parse_github_repo_url(repo_url)
        default_branch = await get_default_branch(owner, repo_name, github_pat)
        logging.info(f"Default branch for {owner}/{repo_name} is {default_branch}")

        page = 1
        while True:
            commits = await get_commits(owner, repo_name, github_pat, page=page, branch=default_branch)
            if not commits:
                break
            for commit in commits:
                sha = commit["sha"]
                commit_date = commit["commit"]["author"]["date"]
                existing = await get_commit_by_sha(sha)
                if existing is None:
                    commit_id = await create_commit(sha, repo_id, datetime.fromisoformat(commit_date.rstrip("Z")))
                else:
                    commit_id = existing["id"]

                try:
                    diff_text = await get_commit_detail(owner, repo_name, sha, github_pat)
                except Exception as e:
                    logging.error(f"Failed to fetch commit detail for {sha}: {e}")
                    continue

                findings = scan_text_for_secrets(diff_text)
                for secret_type, secret_value in findings:
                    masked_value = mask_secret(secret_value)
                    # Use placeholders for file_path and line_no; can be improved later
                    file_path = "unknown"
                    line_no = 0
                    await create_finding(commit_id, secret_type, masked_value, file_path, line_no)

                await mark_commit_scanned(commit_id)

            page += 1

        await update_scan_job_status(scan_id, "completed")
    except Exception as e:
        logging.error(f"Error during scan job {scan_id}: {e}")
        await update_scan_job_status(scan_id, "failed")
    finally:
        await database.disconnect()