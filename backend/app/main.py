from fastapi import FastAPI
from prometheus_client import make_asgi_app, Counter, Histogram
import time

# Create FastAPI app with metadata
app = FastAPI(
    title="AI Research to Video Explainer API",
    description="Backend API for converting research papers to video explanations",
    version="0.1.0"
)

# Mount Prometheus metrics
app.mount("/metrics", make_asgi_app())

# Custom metrics
REQUEST_COUNTER = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

@app.get("/")
def read_root():    
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "ai-explainer-backend"}

# Middleware for automatic metrics collection
@app.middleware("http")
async def add_metrics(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    REQUEST_COUNTER.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.observe(time.time() - start_time)
    return response