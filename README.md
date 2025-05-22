

# Entro Task - AWS Leak Scanner

A containerized service that scans GitHub repositories for leaked AWS credentials by analyzing commit diffs.  
Built with FastAPI, RabbitMQ, PostgreSQL, and an asynchronous worker.

---

## Features

- Trigger scans via REST API by providing a GitHub repo URL and PAT (Personal Access Token).
- Async worker fetches commits, scans diffs for AWS secret patterns.
- Stores scan jobs, commits, and findings in PostgreSQL database.
- Resume scans after interruption by tracking scanned commits.
- API endpoint to check scan status and results.
- Simple web UI to view scan results with masked secret values.
- Uses RabbitMQ to decouple API server and worker.
- Fully containerized with Docker Compose.
---

## Architecture

```
[User/API Client] <---> [FastAPI API Server] <--> [RabbitMQ] <--> [Async Worker]
                                              |
                                              v
                                       [PostgreSQL Database]
                                              |
                                              v
                                         [pgAdmin UI]
```

---

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- GitHub Personal Access Token (PAT) with `repo` or `public_repo` scopes

### Setup

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/entro_task.git
   cd entro_task
   ```

2. Create a `.env` file with environment variables:

   ```
   DATABASE_URL=postgresql://entro:entro@db:5432/entro_db
   RABBITMQ_HOST=rabbitmq
   ```

3. Build and start containers:

   ```bash
   docker-compose up --build -d
   ```

4. Access services:

   - API: http://localhost:8000
   - pgAdmin: http://localhost:5050 (login: admin@admin.com / admin)
   - RabbitMQ UI: http://localhost:15672 (guest/guest)
   - API docs (Swagger UI): http://localhost:8000/docs
   - Scan results UI: http://localhost:8000/ui/scan/{scan_id}/results
   - UI Main Menu: http://localhost:8000/ui/

---

## Usage

### Trigger a scan

```bash
curl -X POST http://localhost:8000/scan/ \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/yourusername/yourrepo", "github_pat": "your_github_pat"}'
```

### Check scan status

```bash
curl http://localhost:8000/status/{scan_id}
```

### View scan results in UI

Open:

```
http://localhost:8000/ui/scan/{scan_id}/results
```

Replace `{scan_id}` with the actual scan ID.

---

## Project Structure

- `api/` – FastAPI route handlers (`scan.py`, `status.py`, `ui.py`)
- `db/` – Database models and CRUD operations
- `worker/` – Async worker consuming RabbitMQ messages and scanning commits
- `templates/` – Jinja2 HTML templates for UI pages
- `docker-compose.yml` – Docker service definitions (API, worker, db, RabbitMQ, pgAdmin)
- `Dockerfile` & `worker/Dockerfile` – Docker images for API and worker

---

## License

MIT License

---