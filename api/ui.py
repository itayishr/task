from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from db.crud import get_scan_job_by_id, get_findings_by_scan_id

router = APIRouter()
templates = Jinja2Templates(directory="templates")  # We'll create this folder next

@router.get("/scan/{scan_id}/results", response_class=HTMLResponse)
async def scan_results(request: Request, scan_id: int):
    scan_job = await get_scan_job_by_id(scan_id)
    if not scan_job:
        raise HTTPException(status_code=404, detail="Scan job not found")

    findings = await get_findings_by_scan_id(scan_id)

    return templates.TemplateResponse("results.html", {
        "request": request,
        "scan_job": scan_job,
        "findings": findings,
    })