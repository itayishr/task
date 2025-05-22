import httpx

GITHUB_API_URL = "https://api.github.com"

def parse_github_repo_url(repo_url: str):
    parts = repo_url.rstrip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]
    return owner, repo

async def get_default_branch(owner: str, repo: str, github_pat: str) -> str:
    headers = {
        "Authorization": f"token {github_pat}",
        "Accept": "application/vnd.github.v3+json",
    }
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        repo_info = response.json()
        return repo_info.get("default_branch", "main")

async def get_commits(owner: str, repo: str, github_pat: str, page=1, per_page=100, branch="main"):
    headers = {
        "Authorization": f"token {github_pat}",
        "Accept": "application/vnd.github.v3+json",
    }
    params = {"sha": branch, "per_page": per_page, "page": page}
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

async def get_commit_detail(owner: str, repo: str, sha: str, github_pat: str):
    headers = {
        "Authorization": f"token {github_pat}",
        "Accept": "application/vnd.github.v3.patch",
    }
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits/{sha}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.text