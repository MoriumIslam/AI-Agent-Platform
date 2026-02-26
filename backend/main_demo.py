"""
AI Agent Platform Backend - Demo Mode
Simplified version for local testing without database
"""

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
import json
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============= STARTUP & SHUTDOWN =============

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    logger.info("🚀 Starting AI Agent Platform Backend (Demo Mode)...")
    yield
    logger.info("🛑 Shutting down...")

# ============= FASTAPI APP INITIALIZATION =============

app = FastAPI(
    title="AI Agent Platform API",
    description="Social Media Lead Management with AI Classification & CRM Sync",
    version="1.0.0 (Demo)",
    lifespan=lifespan
)

# ============= MIDDLEWARE =============

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= DATA STORAGE (IN-MEMORY) =============

messages_db = []
leads_db = []
responses_db = []

# ============= ROOT ENDPOINT =============

@app.get("/")
async def root():
    """API Information"""
    return {
        "name": "AI Agent Platform API",
        "version": "1.0.0 (Demo Mode)",
        "status": "🟢 Running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "GET /health",
            "messages": "GET /api/messages",
            "leads": "GET /api/leads",
            "metrics": "GET /api/metrics",
            "websocket": "WS /ws"
        }
    }

# ============= HEALTH CHECK =============

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "mode": "demo",
        "database": "in-memory"
    }

# ============= MESSAGE ENDPOINTS =============

@app.get("/api/messages")
async def get_messages():
    """Get all messages"""
    return {
        "total": len(messages_db),
        "messages": messages_db[-10:] if messages_db else [
            {
                "id": "msg_001",
                "platform": "instagram",
                "author": "user_123",
                "text": "Amazing product! Can't wait to try it.",
                "score": 87,
                "category": "HOT",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "msg_002",
                "platform": "twitter",
                "author": "user_456",
                "text": "Interested in learning more about pricing",
                "score": 75,
                "category": "WARM",
                "created_at": datetime.now().isoformat()
            }
        ]
    }

@app.post("/api/messages/{message_id}/score")
async def score_message(message_id: str):
    """Score a message with ML model"""
    return {
        "message_id": message_id,
        "score": 85,
        "category": "HOT",
        "confidence": 0.92,
        "sentiment": 0.8,
        "reasoning": "High purchase intent with urgency signals"
    }

@app.post("/api/messages/{message_id}/respond")
async def generate_response(message_id: str):
    """Generate AI response"""
    return {
        "message_id": message_id,
        "response_text": "Thank you for your interest! We'd love to help. What questions do you have?",
        "confidence": 0.95,
        "should_post": True,
        "action": "auto_post",
        "tokens_used": 45
    }

# ============= LEAD ENDPOINTS =============

@app.get("/api/leads")
async def get_leads(category: str = None):
    """Get leads with optional category filter"""
    leads = leads_db if leads_db else [
        {"id": "lead_001", "name": "John Doe", "email": "john@example.com", "score": 92, "category": "HOT"},
        {"id": "lead_002", "name": "Jane Smith", "email": "jane@example.com", "score": 68, "category": "WARM"},
        {"id": "lead_003", "name": "Bob Johnson", "email": "bob@example.com", "score": 45, "category": "COLD"},
    ]
    
    if category:
        leads = [l for l in leads if l["category"] == category]
    
    return {
        "total": len(leads),
        "hot": len([l for l in leads if l["category"] == "HOT"]),
        "warm": len([l for l in leads if l["category"] == "WARM"]),
        "cold": len([l for l in leads if l["category"] == "COLD"]),
        "leads": leads
    }

# ============= CRM ENDPOINTS =============

@app.post("/api/crm/sync")
async def sync_to_crm(lead_id: str = None):
    """Sync lead to CRM"""
    return {
        "status": "success",
        "lead_id": lead_id or "lead_001",
        "synced_to": ["HubSpot", "Salesforce"],
        "sync_time_ms": 3200,
        "timestamp": datetime.now().isoformat()
    }

# ============= METRICS ENDPOINTS =============

@app.get("/api/metrics")
async def get_metrics():
    """Real-time platform metrics"""
    return {
        "messages_processed": 1247,
        "hot_leads_generated": 324,
        "crm_sync_success": 99.9,
        "average_response_time_ms": 3200,
        "responses_auto_posted": 892,
        "timestamp": datetime.now().isoformat()
    }

# ============= WEBHOOK ENDPOINTS =============

@app.post("/webhooks/instagram")
async def instagram_webhook(request: dict):
    """Instagram webhook handler"""
    logger.info(f"📱 Instagram message received: {request}")
    return {"status": "received"}

@app.post("/webhooks/twitter")
async def twitter_webhook(request: dict):
    """Twitter webhook handler"""
    logger.info(f"🐦 Twitter message received: {request}")
    return {"status": "received"}

# ============= WEBSOCKET ENDPOINT =============

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"✅ Client connected. Total: {len(self.active_connections)}")

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"❌ Client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            # Simulate real-time metric updates every 3 seconds
            await asyncio.sleep(3)
            await manager.broadcast({
                "type": "metrics_update",
                "messages_processed": 1247,
                "hot_leads": 324,
                "sync_success_rate": 99.9,
                "timestamp": datetime.now().isoformat()
            })
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await manager.disconnect(websocket)

# ============= ERROR HANDLERS =============

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "timestamp": datetime.now().isoformat()}
    )

# ============= RUN SERVER =============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="info"
    )
