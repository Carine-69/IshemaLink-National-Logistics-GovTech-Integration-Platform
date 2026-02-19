# IshemaLink API 🚚

A national logistics and cargo management platform for Rwanda, connecting domestic and international shipment agents with real-time tracking, mobile money payments, and government integrations (RRA & RURA).

---

## Table of Contents

- [Project Overview](#project-overview)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Local Development Setup](#local-development-setup)
- [Production Deployment](#production-deployment)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Monitoring](#monitoring)

---

## Project Overview

IshemaLink handles end-to-end logistics operations in Rwanda including:
- Domestic & International shipment booking
- MTN/Airtel Mobile Money payment integration
- Real-time truck tracking
- RRA tax compliance (EBM receipts)
- RURA transport license verification
- SMS/Email notifications to agents and exporters

---

## System Architecture

```
                        ┌─────────────────────────────────────────┐
                        │           PRODUCTION STACK               │
                        └─────────────────────────────────────────┘

  Client (Browser/Mobile)
         │
         ▼
  ┌─────────────┐
  │    Nginx    │  ← Reverse Proxy + SSL/TLS (Port 80/443)
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │  Gunicorn   │  ← WSGI Server (Port 8000, 4 workers)
  │  (Django)   │
  └──────┬──────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│  DB   │ │ Redis │  ← Cache + Celery Broker
│(PgBnc)│ └───┬───┘
└───────┘     │
    │          ▼
    ▼      ┌────────┐
┌───────┐  │ Celery │  ← Async tasks (payments, notifications)
│Postgres│  └────────┘
└───────┘

Monitoring: Prometheus → Grafana
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0, Django REST Framework |
| Database | PostgreSQL 14 + PgBouncer |
| Cache/Queue | Redis 7 |
| Task Queue | Celery |
| Web Server | Gunicorn + Nginx |
| Containerization | Docker + Docker Compose |
| Monitoring | Prometheus + Grafana |
| Payments | MTN/Airtel MoMo (Mock) |

---

## Local Development Setup

### Prerequisites
- Docker
- docker-compose

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ishemalink_api.git
cd ishemalink_api

# 2. Create environment file
cp .env.example .env
# Edit .env with your local values

# 3. Build and start
docker-compose build
docker-compose up

# 4. API is available at:
# http://127.0.0.1:8000/api/
```

---

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for full step-by-step guide.

```bash
# Quick start
docker-compose -f docker-compose.prod.yml up -d
```

---

## API Endpoints

### Shipments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/shipments/create/` | Create domestic or international shipment |
| GET | `/api/tracking/{tracking_code}/live/` | Real-time truck location |

### Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/payments/initiate/` | Trigger MoMo push prompt |
| POST | `/api/payments/webhook/` | Receive payment callback |

### Notifications
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/notifications/broadcast/` | Admin alert to all drivers |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/dashboard/summary/` | Live trucks and revenue view |

### Government Integrations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/gov/ebm/sign-receipt/` | Request RRA tax signature |
| GET | `/api/gov/rura/verify-license/{license_no}/` | Verify driver license |
| POST | `/api/gov/customs/generate-manifest/` | Generate EAC customs XML |
| GET | `/api/gov/audit/access-log/` | Government audit trail |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/routes/top/` | High-traffic corridors |
| GET | `/api/analytics/commodities/breakdown/` | Cargo type statistics |
| GET | `/api/analytics/revenue/heatmap/` | Geospatial revenue data |
| GET | `/api/analytics/drivers/leaderboard/` | Top performing drivers |

### Operations & Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/deep/` | DB, Redis, and disk health check |
| GET | `/api/ops/metrics/` | Prometheus formatted metrics |
| POST | `/api/ops/maintenance/toggle/` | Toggle maintenance mode |

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `abc123...` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hostnames | `your-domain.com` |
| `POSTGRES_DB` | Database name | `ishemalink` |
| `POSTGRES_USER` | Database user | `ishema` |
| `POSTGRES_PASSWORD` | Database password | `strongpassword` |
| `POSTGRES_HOST` | Database host | `pgbouncer` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379/0` |

---

## Testing

```bash
# Run all tests
docker-compose run web pytest

# With coverage report
docker-compose run web pytest --cov=. --cov-report=html

# Load testing (requires locust)
locust -f tests/locustfile.py --host=http://localhost:8000
```

---

## Monitoring

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (default login: admin/admin)

---

## License

ALU Academic Project — IshemaLink National Rollout, 2026