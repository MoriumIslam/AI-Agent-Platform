"""
AI Agent Platform Backend - Dynamic Demo Server
Metrics change in real-time to simulate live platform activity
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
from datetime import datetime
import random
import math

# ============= GLOBAL STATE =============

class DynamicMetrics:
    """Manages dynamic, changing metrics"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.message_count = 1247
        self.hot_leads = 324
        self.warm_leads = 892
        self.cold_leads = 1456
        self.responses_posted = 892
        
    def get_time_seconds(self):
        """Get elapsed seconds since start"""
        return (datetime.now() - self.start_time).total_seconds()
    
    def get_metrics(self):
        """Return dynamic metrics that change over time"""
        elapsed = self.get_time_seconds()
        
        # Simulate gradual increase in processed messages
        messages_processed = self.message_count + int(elapsed * 0.5)  # +0.5 per second
        
        # Simulate hot leads increasing slightly
        hot_leads = self.hot_leads + int(elapsed * 0.15)  # +0.15 per second
        
        # Simulate variable response time (50-350ms with some randomness)
        base_response_time = 150 + 100 * math.sin(elapsed * 0.05)
        response_time = int(base_response_time + random.randint(-20, 50))
        
        # Sync success stays high but varies slightly
        sync_success = 99.8 + random.uniform(-0.5, 0.5)
        
        # Auto-posted responses increase
        auto_posted = self.responses_posted + int(elapsed * 0.3)
        
        return {
            "messages_processed": messages_processed,
            "hot_leads_generated": hot_leads,
            "crm_sync_success": round(sync_success, 2),
            "average_response_time_ms": max(50, response_time),
            "responses_auto_posted": auto_posted,
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": int(elapsed),
            "server_health": "excellent" if sync_success > 99 else "good"
        }
    
    def get_leads(self):
        """Return dynamic lead distribution"""
        elapsed = self.get_time_seconds()
        hot = self.hot_leads + int(elapsed * 0.15)
        warm = self.warm_leads + int(elapsed * 0.08)
        cold = self.cold_leads + int(elapsed * 0.05)
        
        return {
            "total": hot + warm + cold,
            "hot": hot,
            "warm": warm,
            "cold": cold,
            "leads": [
                {"id": "lead_001", "name": "John Doe", "email": "john@example.com", "score": 92, "category": "HOT"},
                {"id": "lead_002", "name": "Jane Smith", "email": "jane@example.com", "score": 68, "category": "WARM"},
                {"id": "lead_003", "name": "Bob Johnson", "email": "bob@example.com", "score": 45, "category": "COLD"},
                {"id": "lead_004", "name": "Alice Brown", "email": "alice@example.com", "score": 88, "category": "HOT"},
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    def get_messages(self):
        """Return dynamic messages"""
        elapsed = self.get_time_seconds()
        message_count = int(elapsed * 0.5)
        
        platforms = ["instagram", "twitter", "linkedin", "facebook"]
        sample_texts = [
            "Amazing product! Can't wait to try it.",
            "Interested in learning more about pricing",
            "When will this be available?",
            "This looks exactly what we need!",
            "Tell me more about your features",
            "How does this compare to competitors?",
            "Is there a free trial available?",
            "Looking for a solution like this",
            "Can you send me more information?",
            "This is perfect for our business!"
        ]
        
        messages = []
        for i in range(min(5, message_count + 2)):
            platform = random.choice(platforms)
            text = random.choice(sample_texts)
            score = random.randint(50, 95)
            category = "HOT" if score > 80 else "WARM" if score > 60 else "COLD"
            
            messages.append({
                "id": f"msg_{1000+i}",
                "platform": platform,
                "author": f"user_{random.randint(1000, 9999)}",
                "text": text,
                "score": score,
                "category": category,
                "created_at": datetime.now().isoformat()
            })
        
        return {
            "total": self.message_count + int(elapsed * 0.5),
            "messages": messages,
            "timestamp": datetime.now().isoformat()
        }

# Create global metrics instance
metrics = DynamicMetrics()

# ============= API HANDLER =============

class APIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for API endpoints"""
    
    def do_GET(self):
        """Handle GET requests with error handling"""
        try:
            path = urlparse(self.path).path
            
            # Health check
            if path == "/health":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                response = {
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat(),
                    "uptime_seconds": int(metrics.get_time_seconds()),
                    "mode": "dynamic",
                    "error": None
                }
                self.wfile.write(json.dumps(response).encode())
            
            # Root endpoint
            elif path == "/":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                response = {
                    "name": "AI Agent Platform API",
                    "version": "1.0.0 (Dynamic)",
                    "status": "🟢 Running",
                    "timestamp": datetime.now().isoformat(),
                    "mode": "🔄 DYNAMIC - Metrics change in real-time",
                    "uptime_seconds": int(metrics.get_time_seconds()),
                    "endpoints": {
                        "health": "GET /health",
                        "messages": "GET /api/messages [DYNAMIC]",
                        "leads": "GET /api/leads [DYNAMIC]",
                        "metrics": "GET /api/metrics [DYNAMIC]"
                    },
                    "error": None
                }
                self.wfile.write(json.dumps(response).encode())
            
            # Messages endpoint - DYNAMIC
            elif path == "/api/messages":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                response = metrics.get_messages()
                response["error"] = None
                self.wfile.write(json.dumps(response).encode())
            
            # Leads endpoint - DYNAMIC
            elif path == "/api/leads":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                response = metrics.get_leads()
                response["error"] = None
                self.wfile.write(json.dumps(response).encode())
            
            # Metrics endpoint - DYNAMIC
            elif path == "/api/metrics":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                response = metrics.get_metrics()
                response["error"] = None
                self.wfile.write(json.dumps(response).encode())
            
            # AI Agent Score simulation
            elif "/api/messages/" in path and "/score" in path:
                try:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    score = random.randint(50, 95)
                    response = {
                        "message_id": path.split("/")[3],
                        "score": score,
                        "category": "HOT" if score > 80 else "WARM" if score > 60 else "COLD",
                        "confidence": random.uniform(0.85, 0.98),
                        "sentiment": random.uniform(0.5, 1.0),
                        "reasoning": "High purchase intent with urgency signals",
                        "timestamp": datetime.now().isoformat(),
                        "error": None
                    }
                    self.wfile.write(json.dumps(response).encode())
                except Exception as e:
                    self._error_response(400, f"Score calculation failed: {str(e)}")
            
            # Response generation
            elif "/api/messages/" in path and "/respond" in path:
                try:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    responses = [
                        "Thank you for your interest! We'd love to help. What questions do you have?",
                        "That's great to hear! Let me schedule a demo for you.",
                        "Perfect timing! We're running a special promotion right now.",
                        "I'm glad you're interested. Can you tell me more about your needs?",
                        "Excellent question! Our solution is designed specifically for that."
                    ]
                    response = {
                        "message_id": path.split("/")[3],
                        "response_text": random.choice(responses),
                        "confidence": random.uniform(0.90, 0.99),
                        "should_post": True,
                        "action": "auto_post" if random.random() > 0.2 else "human_review",
                        "tokens_used": random.randint(30, 50),
                        "timestamp": datetime.now().isoformat(),
                        "error": None
                    }
                    self.wfile.write(json.dumps(response).encode())
                except Exception as e:
                    self._error_response(400, f"Response generation failed: {str(e)}")
            
            # CRM Sync
            elif path == "/api/crm/sync":
                try:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    response = {
                        "status": "success" if random.random() > 0.01 else "partial",
                        "synced_to": ["HubSpot", "Salesforce", "Pipedrive"],
                        "sync_time_ms": random.randint(2000, 4000),
                        "contacts_synced": random.randint(50, 200),
                        "deals_created": random.randint(5, 20),
                        "timestamp": datetime.now().isoformat(),
                        "error": None
                    }
                    self.wfile.write(json.dumps(response).encode())
                except Exception as e:
                    self._error_response(500, f"CRM sync failed: {str(e)}")
            
            else:
                self._error_response(404, f"Endpoint not found: {path}")
        
        except Exception as e:
            self._error_response(500, f"Internal server error: {str(e)}")
    
    def do_POST(self):
        """Handle POST requests with error handling"""
        try:
            path = urlparse(self.path).path
            
            if "/respond" in path or "/score" in path or "/sync" in path:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                response = {
                    "status": "success",
                    "timestamp": datetime.now().isoformat(),
                    "processing_time_ms": random.randint(100, 500),
                    "error": None
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self._error_response(404, f"POST endpoint not found: {path}")
        
        except Exception as e:
            self._error_response(500, f"POST request failed: {str(e)}")
    
    def _error_response(self, status_code, message):
        """Send JSON error response"""
        try:
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            response = {
                "error": message,
                "status_code": status_code,
                "timestamp": datetime.now().isoformat(),
                "error_type": self._get_error_type(status_code)
            }
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            print(f"❌ Error sending error response: {e}")
    
    def _get_error_type(self, status_code):
        """Get error type from status code"""
        error_types = {
            400: "BAD_REQUEST",
            404: "NOT_FOUND",
            500: "INTERNAL_SERVER_ERROR",
            502: "BAD_GATEWAY",
            503: "SERVICE_UNAVAILABLE"
        }
        return error_types.get(status_code, "UNKNOWN_ERROR")
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")


# ============= SERVER STARTUP =============

def run_server():
    """Start the HTTP server"""
    server_address = ("", 5000)
    httpd = HTTPServer(server_address, APIHandler)
    print("🚀 Backend Server running on http://0.0.0.0:5000")
    print("🔄 Mode: DYNAMIC - Metrics change in real-time every 3 seconds")
    print("📝 Available endpoints:")
    print("   - GET  http://localhost:5000/")
    print("   - GET  http://localhost:5000/health")
    print("   - GET  http://localhost:5000/api/messages       [DYNAMIC]")
    print("   - GET  http://localhost:5000/api/leads          [DYNAMIC]")
    print("   - GET  http://localhost:5000/api/metrics        [DYNAMIC]")
    print("   - POST http://localhost:5000/api/messages/{id}/score")
    print("   - POST http://localhost:5000/api/messages/{id}/respond")
    print("   - POST http://localhost:5000/api/crm/sync")
    print("\nPress Ctrl+C to stop\n")
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
