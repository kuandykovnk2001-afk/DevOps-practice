# DevOps Practice — Containerized Infrastructure (Nginx + Flask + PostgreSQL)

A three-service containerized infrastructure built with Docker Compose, demonstrating the Infrastructure as Code principle: the entire environment can be deployed identically on any clean server with a single `git clone` and one script execution — no manual configuration required.

## Architecture

```
User Request → Nginx (reverse proxy, port 80)
             → Flask App (REST API, port 5000)
             → PostgreSQL 15 (database, port 5432)
```

| Service         | Port  | Role                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Nginx           | 80    | Reverse proxy — entry point for all incoming HTTP requests   |
| Flask App       | 5000  | Application layer — handles API requests, business logic     |
| PostgreSQL 15   | 5432  | Persistent relational database (Docker volume)                |

Containers communicate over the Docker Compose network using service names as hostnames (e.g. the Flask app connects to the database via `host="postgres"`, not an IP address).

## Requirements

- Docker
- Docker Compose
- Git

No other local dependencies are needed — Python, Flask, and PostgreSQL all run inside containers.

## Installation & Deployment

On any clean server (tested on Ubuntu Server):

```bash
git clone https://github.com/kuandykovnk2001-afk/DevOps-practice.git
cd DevOps-practice
./start.sh
```

`start.sh` runs:

```bash
sudo docker compose up -d --build
```

All three containers (Nginx, Flask, PostgreSQL) will start automatically in the correct order — PostgreSQL first, then the Flask app, then Nginx — thanks to the `depends_on` directives in `docker-compose.yml`.

## API Endpoints

| Endpoint     | Method | Description                                  |
|--------------|--------|-----------------------------------------------|
| `/`          | GET    | Health check — confirms the app is running    |
| `/add`       | POST   | Accepts a JSON payload, saves it to PostgreSQL |
| `/messages`  | GET    | Retrieves all stored messages from PostgreSQL  |

### Example usage

```bash
# Health check
curl http://localhost:5000

# Save a message
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello from DevOps!"}'

# Retrieve all messages
curl http://localhost:5000/messages
```

## Project Structure

```
DevOps-practice/
├── docker-compose.yml   # Defines all three services (Infrastructure as Code)
├── nginx.conf           # Reverse proxy configuration
├── app/                 # Flask application source
├── start.sh             # One-command deployment script
└── README.md
```

## Configuration

Database credentials are set as environment variables in `docker-compose.yml` (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`). For any real deployment beyond a local demo/testing environment, these should be moved to a `.env` file and excluded from version control rather than hardcoded.

## Notes

- This project was built and validated across two separate virtual machines: one as the development environment, and a second, clean VM used purely to confirm that deployment is fully reproducible without manual setup.
- Data persists across container restarts via a named Docker volume (`postgres_data`).

## Author

Developed as an individual technical exercise during a DevOps Infrastructure internship at JSC "National Information Technologies" (NIT).
