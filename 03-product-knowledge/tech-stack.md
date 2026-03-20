# MeetFlow - Technology Stack

## Frontend

| Layer | Technology | Notes |
|-------|-----------|-------|
| Web app | Next.js 14 (App Router) + TypeScript | Dashboard, meeting detail pages, settings |
| UI library | Material UI (MUI) | Component library for consistent design |
| State management | Zustand | Lightweight, used for client-side meeting state |
| Real-time updates | Socket.IO | Live transcription feed during active meetings |

## Backend

| Layer | Technology | Notes |
|-------|-----------|-------|
| API server | Python + FastAPI | REST APIs for all client operations |
| Task queue | Celery + Redis | Async processing for summary generation, action item extraction |
| Database | PostgreSQL | Primary data store - users, meetings, transcripts, action items |
| Cache | Redis | Session cache, rate limiting, real-time pub/sub |
| File storage | AWS S3 | Audio recordings, exported files |
| Search | Elasticsearch | Full-text search across meeting transcripts |

## AI/ML Pipeline

| Component | Technology | Notes |
|-----------|-----------|-------|
| Transcription | Whisper (fine-tuned) | 92% accuracy in quiet environments, drops below 80% in noisy |
| Speaker diarization | PyAnnote | Fails for 8+ attendees - speakers get merged |
| Summary generation | Fine-tuned LLM | Averages 350 words per 30-min meeting, takes 45-90 sec |
| Action item extraction | Custom classifier | Trained on 50K labeled meetings, 66% accuracy (34% error rate) |
| Confidence scoring | Gradient boosted model | High/medium/low scores, gaps with implicit and conditional actions |
| Model serving | FastAPI + ONNX Runtime | Model retraining pipeline is manual, takes 2 weeks to deploy |
| Training data | Label Studio | Internal labeling tool for meeting annotation |

## Integrations

| Service | Method | Status |
|---------|--------|--------|
| Zoom | OAuth + Webhooks | Live - auto-join, cloud recording |
| Google Meet | Chrome extension + API | Live |
| Microsoft Teams | Graph API | Live |
| Slack | Slack API (Bot) | Live - summary digests, action item posts |
| Notion | Notion API | Live - push summaries to pages |
| Jira | REST API | Live - create tasks from action items |
| Linear | GraphQL API | Live - create issues from action items |
| Salesforce | REST API | Planned Q2 2026 - Dana's team building this |

## Infrastructure

| Component | Technology | Notes |
|-----------|-----------|-------|
| Cloud | AWS | EC2, RDS, S3, SQS, CloudFront |
| Container orchestration | Kubernetes (EKS) | Auto-scaling for meeting processing spikes |
| CI/CD | GitHub Actions | Automated testing, staging deploys |
| Monitoring | Datadog | APM, logs, custom dashboards |
| Error tracking | Sentry | Client and server error capture |
| CDN | CloudFront | Static assets, web app delivery |

## Architecture Pattern

MeetFlow follows Clean Architecture with four layers:

```
Presentation (Next.js, API routes)
    |
Application (FastAPI services, Celery tasks)
    |
Domain (Meeting, Transcript, ActionItem, Summary models)
    |
Infrastructure (PostgreSQL, Redis, S3, ML models, third-party APIs)
```

Dependencies point inward. Outer layers implement inner layer interfaces. The ML pipeline runs as a separate service behind an internal API, decoupled from the main application server.

## Tech Debt (from product.md)

- Transcription accuracy drops below 80% in noisy environments
- Speaker diarization fails for 8+ attendees
- Summary generation takes 45-90 seconds (users expect near-instant)
- Model retraining pipeline is manual, takes 2 weeks per deploy
- No automated evaluation pipeline for action item accuracy
