# API Documentation - AI Agent Platform

## Base URL

```
http://localhost:5000
```

## Authentication

All endpoints (except webhooks) require JWT token in `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

---

## Endpoints

### Health & Status

#### GET `/health`
Check API health status

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-25T10:30:45.123456",
  "version": "1.0.0"
}
```

#### GET `/`
Get API information and endpoints

---

### Messages

#### GET `/api/messages`
Get recent messages (paginated)

**Parameters:**
- `limit` (int, default: 50) - Number of messages to return

**Response:**
```json
{
  "messages": [
    {
      "id": 1,
      "platform": "instagram",
      "author": "@johndoe",
      "text": "I need help with API integration",
      "timestamp": "2026-02-25T10:25:00Z"
    }
  ],
  "total": 1,
  "limit": 50
}
```

#### POST `/api/messages/{message_id}/score`
Score a message using ML model

**Request Body:**
```json
{
  "text": "I'm very interested in your API pricing"
}
```

**Response:**
```json
{
  "score": 87,
  "category": "HOT",
  "confidence": 0.92,
  "sentiment": 0.8,
  "reasoning": "Purchase intent detected, Sentiment: 0.8, Engagement: 3 interactions"
}
```

#### POST `/api/messages/{message_id}/respond`
Generate AI response for a message

**Request Body:**
```json
{
  "text": "What are your pricing plans?",
  "brand_voice": "professional"
}
```

**Response:**
```json
{
  "response_text": "Great question! Our pricing plans start at $29/month. Would you like more details?",
  "confidence": 0.88,
  "should_post": true,
  "action": "auto_post",
  "model_used": "gpt-4",
  "tokens_used": 45
}
```

---

### Leads

#### GET `/api/leads`
Get leads with optional filtering

**Parameters:**
- `category` (string, optional) - Filter by: HOT, WARM, COLD
- `limit` (int, default: 50) - Number of leads to return

**Response:**
```json
{
  "leads": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@company.com",
      "category": "HOT",
      "score": 87,
      "platform": "instagram",
      "crm_synced": true
    }
  ],
  "total": 2,
  "category_filter": null
}
```

#### POST `/api/leads/{lead_id}/tag`
Manually tag a lead

**Request Body:**
```json
{
  "category": "HOT",
  "notes": "Customer interested in enterprise plan"
}
```

---

### CRM Integration

#### POST `/api/crm/sync`
Sync a lead to CRM system

**Request Body:**
```json
{
  "lead_id": "123",
  "crm": "hubspot",
  "force_update": false
}
```

**Response:**
```json
{
  "status": "success",
  "crm": "hubspot",
  "crm_id": "hubspot_123_1708792200",
  "sync_time_ms": 1200
}
```

#### GET `/api/crm/sync-status/{lead_id}`
Check CRM sync status for a lead

**Response:**
```json
{
  "lead_id": "123",
  "synced_to": ["hubspot", "salesforce"],
  "last_sync": "2026-02-25T10:30:00Z",
  "status": "success"
}
```

#### POST `/api/crm/connect`
Connect a CRM system

**Request Body:**
```json
{
  "crm": "hubspot",
  "auth_code": "oauth_auth_code_from_hubspot"
}
```

---

### Metrics & Analytics

#### GET `/api/metrics`
Get real-time platform metrics

**Response:**
```json
{
  "messagesProcessed": 1243,
  "hotLeads": 324,
  "warmLeads": 892,
  "coldLeads": 1456,
  "crmSyncSuccess": 99.9,
  "avgResponseTime": 3.2,
  "timestamp": "2026-02-25T10:30:45Z"
}
```

#### GET `/api/analytics/dashboard`
Get comprehensive analytics dashboard

**Response:**
```json
{
  "period": "today",
  "messages_processed": 1243,
  "responses_generated": 1200,
  "auto_posted": 1089,
  "human_reviewed": 111,
  "leads_scored": 456,
  "leads_by_category": {
    "HOT": 324,
    "WARM": 892,
    "COLD": 1456
  },
  "crm_syncs": {
    "attempted": 234,
    "succeeded": 233,
    "failed": 1,
    "success_rate_percent": 99.6
  }
}
```

---

### Webhooks

#### POST `/webhooks/instagram`
Receive webhook from Instagram/Meta

Instagram will POST to this endpoint with message events.

**Webhook Payload Example:**
```json
{
  "entry": [
    {
      "changes": [
        {
          "field": "comments",
          "value": {
            "text": "I need help with your API",
            "id": "comment_789",
            "username": "john_doe"
          }
        }
      ]
    }
  ]
}
```

**Verification (GET request):**
```
GET /webhooks/instagram?hub_verify_token=your_token&hub_challenge=challenge_string
```

Response: `challenge_string` (echo back the challenge)

#### POST `/webhooks/twitter`
Receive webhook from Twitter/X

Similar to Instagram webhook format.

---

### WebSocket

#### WS `/ws`
Real-time WebSocket connection for live updates

**Connect:**
```javascript
const socket = new WebSocket('ws://localhost:5000/ws');

socket.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Update:', message);
};
```

**Message Types:**
- `message_scored` - Lead was scored
- `response_generated` - Reply was generated
- `crm_sync` - Lead was synced to CRM
- `metrics_update` - Metrics changed

**Example Message:**
```json
{
  "type": "message_scored",
  "message_id": "msg_123",
  "score": 87,
  "category": "HOT",
  "confidence": 0.92
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters",
  "error_code": "INVALID_PARAMS"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or missing authentication token",
  "error_code": "AUTH_FAILED"
}
```

### 403 Forbidden
```json
{
  "detail": "Webhook signature verification failed",
  "error_code": "INVALID_SIGNATURE"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded",
  "retry_after": 60
}
```

### 500 Server Error
```json
{
  "detail": "Internal server error",
  "error_code": "INTERNAL_ERROR"
}
```

---

## Rate Limiting

- **Per User:** 1000 requests/minute (burst: 100)
- **Per IP:** 100 requests/minute
- **Headers:**
  - `X-RateLimit-Limit`: Total limit
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Unix timestamp of reset time

---

## Example Usage

### cURL

```bash
# Get metrics
curl -H "Authorization: Bearer your_jwt_token" \
  http://localhost:5000/api/metrics

# Score a message
curl -X POST \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{"text":"I am interested in your product"}' \
  http://localhost:5000/api/messages/1/score
```

### JavaScript

```javascript
// Fetch metrics
const response = await fetch('http://localhost:5000/api/metrics', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
const metrics = await response.json();

// WebSocket connection
const socket = new WebSocket('ws://localhost:5000/ws');
socket.onmessage = (e) => {
  console.log('Live update:', JSON.parse(e.data));
};
```

### Python

```python
import requests

headers = {"Authorization": f"Bearer {token}"}

# Get metrics
response = requests.get('http://localhost:5000/api/metrics', headers=headers)
metrics = response.json()

# Score a message
data = {"text": "I need help with your API"}
response = requests.post(
  'http://localhost:5000/api/messages/1/score',
  json=data,
  headers=headers
)
score_result = response.json()
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

**Last Updated:** February 25, 2026  
**API Version:** 1.0.0
