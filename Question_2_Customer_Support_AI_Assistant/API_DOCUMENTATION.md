# API Documentation

Base URL:

```text
http://127.0.0.1:8010
```

Swagger:

```text
http://127.0.0.1:8010/docs
```

## Upload Document

```http
POST /documents/upload
```

Form field:

```text
file = PDF, DOCX or TXT file
```

## Chat

```http
POST /chat
```

```json
{
  "session_id": "demo-session",
  "question": "How long does standard shipping take?"
}
```

## Conversation History

```http
GET /sessions/demo-session/history
```

## Escalations

```http
GET /escalations
```

