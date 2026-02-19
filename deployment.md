# IshemaLink Deployment Manual
## How to Deploy on a Clean Ubuntu 22.04 Server

---

## Prerequisites

- Ubuntu 22.04 LTS server (AOS Rwanda / KTRN data center)
- Minimum: 2 CPU, 4GB RAM, 20GB disk
- A domain name or public IP address
- SSH access to the server

---

## Step 1: Connect to Your Server

```bash
ssh ubuntu@your-server-ip
```

---

## Step 2: Install Docker and Docker Compose

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y curl git

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (no sudo needed)
sudo usermod -aG docker $USER
newgrp docker

# Install docker-compose
sudo apt install -y docker-compose

# Verify
docker --version
docker-compose --version
```

---

## Step 3: Clone the Repository

```bash
cd /home/ubuntu
git clone https://github.com/your-username/ishemalink_api.git
cd ishemalink_api
```

---

## Step 4: Configure Environment Variables

```bash
# Copy the production env template
cp .env.prod.example .env.prod

# Edit with your actual values
nano .env.prod
```

Fill in these values:
```
SECRET_KEY=<generate with: python3 -c "import secrets; print(secrets.token_urlsafe(50))">
DEBUG=False
ALLOWED_HOSTS=your-domain.com
POSTGRES_DB=ishemalink
POSTGRES_USER=ishema
POSTGRES_PASSWORD=<strong-password>
POSTGRES_HOST=pgbouncer
REDIS_URL=redis://redis:6379/0
```

---

## Step 5: Set Up SSL Certificates

```bash
# Install certbot (for Let's Encrypt free SSL)
sudo apt install -y certbot

# Generate certificate (replace with your domain)
sudo certbot certonly --standalone -d your-domain.com

# Copy certs to nginx folder
mkdir -p nginx/certs
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/certs/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/certs/
sudo chown $USER:$USER nginx/certs/*
```

> **No domain?** Generate a self-signed cert for testing:
> ```bash
> mkdir -p nginx/certs
> openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
>   -keyout nginx/certs/privkey.pem \
>   -out nginx/certs/fullchain.pem \
>   -subj "/CN=your-server-ip"
> ```

---

## Step 6: Update Nginx Config

```bash
nano nginx/nginx.conf
# Replace 'your-domain.com' with your actual domain or IP
```

---

## Step 7: Build and Launch

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start all services in background
docker-compose -f docker-compose.prod.yml up -d

# Check all containers are running
docker-compose -f docker-compose.prod.yml ps
```

---

## Step 8: Run Migrations

```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

---

## Step 9: Verify Deployment

```bash
# Test the API
curl https://your-domain.com/api/health/deep/

# View logs
docker-compose -f docker-compose.prod.yml logs -f web
```

---

## Step 10: Set Up Automated Backups

```bash
# Make backup script executable
chmod +x backup.sh

# Add to cron (runs daily at 2am)
crontab -e
# Add this line:
0 2 * * * /home/ubuntu/ishemalink_api/backup.sh >> /var/log/ishemalink_backup.log 2>&1
```

---

## Step 11: Auto-restart on Server Reboot

```bash
# Enable docker to start on boot
sudo systemctl enable docker

# Containers already have restart: always in compose file
# They will auto-restart after any crash or reboot
```

---

## Monitoring

| Service | URL |
|---------|-----|
| API | https://your-domain.com/api/ |
| Prometheus | http://your-server-ip:9090 |
| Grafana | http://your-server-ip:3000 |

---

## Useful Commands

```bash
# Stop everything
docker-compose -f docker-compose.prod.yml down

# Restart a single service
docker-compose -f docker-compose.prod.yml restart web

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Run Django management commands
docker-compose -f docker-compose.prod.yml exec web python manage.py <command>
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Container won't start | Check logs: `docker-compose logs web` |
| 502 Bad Gateway | Gunicorn not running, check web container |
| Database connection error | Check `.env.prod` credentials |
| SSL error | Verify cert paths in `nginx/certs/` |