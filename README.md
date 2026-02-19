# IshemaLink API 
### National Logistics & Cargo Management Platform for Rwanda
**Author: Carine Umugabekazi | ALU Advanced Python Programming, 2026**

---

## Project Overview

IshemaLink is a production-ready logistics API built for Rwanda's national rollout, handling 50,000+ kg of produce movement. It unifies domestic and international shipment workflows under a single platform with Mobile Money payments, real-time tracking, government integrations (RRA & RURA), and a BI analytics layer for MINICOM reporting.

---

## Project Structure

```
ishemalink_api/
├── Core/                        # Unified shipment & driver models, BookingService
│   ├── models.py                # Shipment + Driver models (domestic & international)
│   ├── booking_service.py       # BookingService — orchestrates full booking flow
│   ├── views.py                 # All API views
│   └── tests.py                 # Test suite
├── Domestic/                    # Domestic module (Rwanda internal shipments)
├── International/               # International module (EAC cross-border shipments)
├── payments/                    # MomoMock payment gateway adapter
├── notifications/               # NotificationEngine (SMS + Email)
├── nginx/                       # Nginx reverse proxy config + SSL
├── monitoring/                  # Prometheus config
├── docker-compose.yml           # Local development stack
├── docker-compose.prod.yml      # Production stack (Nginx, PgBouncer, Redis, Celery)
├── Dockerfile                   # Web container
├── wait-for-db.sh               # DB readiness script
└── backup.sh                    # Automated PostgreSQL backup
```

---

## Architecture

```
Agent/Exporter
      │
      ▼
   Nginx (SSL/TLS)
      │
      ▼
   Gunicorn / Django
      │
   BookingService
   ┌──┴──────────────────────────┐
   │                             │
Domestic Logic          International Logic
(1,000 RWF/kg)          (3,000 RWF/kg + Customs XML)
   │                             │
   └──────────┬──────────────────┘
              │
        MomoMock (MTN/Airtel)
              │
        Async Webhook → Confirm Booking → Assign Driver
              │
        NotificationEngine (SMS + Email)
              │
        PostgreSQL ← PgBouncer ← Redis ← Celery
```

See [ARCHITECTURE.mermaid](ARCHITECTURE.mermaid) for full interactive diagram.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0 |
| Database | PostgreSQL 14 + PgBouncer |
| Cache / Queue | Redis 7 |
| Async Tasks | Celery |
| Web Server | Gunicorn + Nginx |
| Containerization | Docker + Docker Compose |
| Payments | MTN/Airtel MoMo (MomoMock) |
| Monitoring | Prometheus + Grafana |
| Notifications | SMS + Email (NotificationEngine) |

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

# 2. Build and start
docker-compose build
docker-compose up

# 3. API available at:
http://127.0.0.1:8000/api/
```

---

## API Endpoints

### Core
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/` | API root — name and version |
| GET | `/api/status/` | Health check — DB connectivity |

### Shipments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/shipments/create/` | Create domestic or international shipment |
| POST | `/api/payments/webhook/` | Receive MoMo payment callback |
| GET | `/tracking/<id>/live/` | Real-time truck coordinates |

### Admin & Notifications
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard/` | HTML admin control tower dashboard |
| GET | `/dashboard/summary/` | Live active trucks, revenue, available drivers |
| POST | `/notifications/broadcast/` | SMS broadcast to all drivers |

### Government Integrations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/gov/ebm/sign-receipt/` | RRA EBM digital tax receipt |
| GET | `/gov/rura/verify-license/<license_no>/` | RURA driver license verification |
| POST | `/gov/customs/generate-manifest/` | EAC-compliant customs XML manifest |
| GET | `/gov/audit/access-log/` | Government audit trail |

### Analytics & BI
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/routes/top/` | Highest traffic corridors |
| GET | `/analytics/commodities/breakdown/` | Cargo type statistics |
| GET | `/analytics/revenue/heatmap/` | Revenue per sector/district |
| GET | `/analytics/drivers/leaderboard/` | Top drivers by on-time delivery |

---

## Booking Flow

```
POST /api/shipments/create/
        │
        ▼
BookingService.create_shipment()   ← @transaction.atomic
        │
        ├── Determine type (domestic/international)
        ├── Calculate tariff (1000 or 3000 RWF × weight)
        ├── Create Shipment in DB (status: pending_payment)
        └── Initiate MoMo payment via MomoMock
                │
                ▼
        POST /api/payments/webhook/   ← Async callback
                │
        BookingService.handle_payment_callback()
                │
                ├── SUCCESS → Assign first available Driver
                │            → status: confirmed
                │            → Send SMS + Email
                │
                ├── SUCCESS (no driver) → status: confirmed_no_driver
                │
                └── FAILURE → status: payment_failed
                             → Send SMS to agent
```

---

## Shipment Status Lifecycle

```
pending_payment → confirmed
                → confirmed_no_driver
                → payment_failed
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key (from env, never hardcoded) |
| `DEBUG` | `False` in production |
| `ALLOWED_HOSTS` | Comma-separated allowed domains |
| `POSTGRES_DB` | Database name |
| `POSTGRES_USER` | Database user |
| `POSTGRES_PASSWORD` | Database password |
| `POSTGRES_HOST` | `pgbouncer` in production |
| `REDIS_URL` | Redis connection URL |

---

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for the full step-by-step guide to deploy on a clean Ubuntu 22.04 server (AOS Rwanda / KTRN).

```bash
docker-compose -f docker-compose.prod.yml up -d
```

Production stack includes: Nginx + SSL, Gunicorn (4 workers), PostgreSQL + PgBouncer, Redis, Celery, Prometheus, Grafana, automated MinIO backups.

---

## Testing

```bash
# Run tests inside container
docker-compose run web python manage.py test

# With coverage
docker-compose run web pytest --cov=. --cov-report=html
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | Step-by-step Ubuntu server deployment guide |
| [ARCHITECTURE.mermaid](ARCHITECTURE.mermaid) | Full system architecture diagram |
| [swagger.yaml](swagger.yaml) | OpenAPI specification for all endpoints |
| [SUBMISSION_REPORTS.md](SUBMISSION_REPORTS.md) | Integration Report, Scalability Plan, Local Context Essay |

---

## Monitoring

| Service | URL |
|---------|-----|
| API | `https://your-domain.com/api/` |
| Prometheus | `http://your-server:9090` |
| Grafana | `http://your-server:3000` |

---

## Rwanda Context

IshemaLink is built specifically for Rwanda's logistics reality:
- **Mobile Money first** — MTN/Airtel MoMo is the primary payment infrastructure, not a fallback
- **Government compliance built-in** — RRA (EBM receipts) and RURA (license checks) embedded in the booking flow
- **Offline resilience** — mobile agents in low-connectivity districts can sync when connected
- **Data sovereignty** — all data hosted within Rwanda (AOS/KTRN), no foreign cloud for primary storage
- **SMS-first notifications** — works on 2G and basic phones across all districts

---

## License

ALU Academic Project — IshemaLink National Rollout, January 2026
