# Real-Time Notification Service

A production-grade, event-driven notification platform built with Django. Accepts events from any upstream service, fans them out to connected clients in real time over WebSockets, and guarantees delivery even when users are offline.

---

## Architecture Overview

```
Incoming Event (DRF REST API)
          ↓
    aiokafka Producer
          ↓
    aiokafka Consumer
          ↓
   Is user online? (Redis)
   ↙               ↘
WebSocket         Celery Queue
(live delivery)   (deliver on reconnect)
          ↓
   PostgreSQL (notification history)
```

---

## Tech Stack

- Django
- Django Channels 
- Redis
- Celery
- PostgreSQL
- aiokafka
- WebSocket
- Docker 

---

## Features

- **Event Ingestion** — any service can fire an event via a single REST endpoint
- **Real-Time Delivery** — connected users receive notifications instantly over WebSockets
- **Offline Queuing** — notifications for offline users are queued in Redis and delivered on reconnect
- **Delivery Guarantees** — Celery handles retry logic with exponential backoff for failed deliveries
- **Per-User Preferences** — users can opt in or out per notification type
- **Notification History** — all notifications persisted in PostgreSQL and queryable via API
- **Dead Letter Queue** — undeliverable messages after max retries are logged separately for inspection


---

## Build Phases

### Phase 1 — Core API & Data Models
- Django project setup with DRF
- `Event`, `Notification`, `NotificationPreference` models
- REST endpoint to accept incoming events
- PostgreSQL wired via Django ORM

### Phase 2 — Kafka Message Bus
- aiokafka producer publishes event on API receipt
- aiokafka consumer reads from topic and triggers notification logic
- Basic routing: which users should receive this event type?

### Phase 3 — Real-Time WebSocket Delivery
- Django Channels consumers for authenticated WebSocket connections
- Redis channel layer for message passing
- Track online/offline state per user in Redis

### Phase 4 — Offline Queuing & Delivery Guarantees
- Celery task queues notifications for offline users
- Exponential backoff retry on failed delivery
- Dead Letter Queue for messages exceeding max retries
- Deliver queued notifications on user reconnect

### Phase 5 — Per-User Preferences
- Users configure which event types they want notifications for
- Consumer checks preferences before dispatching

### Phase 6 — DevOps & Deployment
- GitHub Actions CI: lint, test, Docker build on every push
- GitHub Actions CD: deploy to AWS ECS on merge to main
- Terraform provisions ECS cluster, ECR repo, RDS (PostgreSQL), ElastiCache (Redis)

---

## Local Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/Real-Time-Notification-Service
.git
cd Real-Time-Notification-Service


# Start all services
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```



## Concepts Demonstrated

- Event-driven architecture with Kafka as the central message bus
- Async WebSocket handling with Django Channels
- Reliable task processing with Celery and Redis
- Fault tolerance via DLQ and exponential backoff
- Stateful user tracking with Redis
- Infrastructure as code with Terraform
- Automated deployment pipeline with GitHub Actions

---

## Author

Built by Lankwei
