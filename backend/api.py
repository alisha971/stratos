# Create this file: insightbridge/backend/api.py

from fastapi import FastAPI
from .schema import (
    TopicRequest, 
    ReportResponse, 
    DeepDiveRequest, 
    DeepDiveResponse
)

app = FastAPI(
    title="InsightBridge API",
    description="Agentic AI for business research and deep-dive analysis."
)

# --- ENDPOINT 1: Main Report Generation ---
@app.post("/analyze-topic", response_model=ReportResponse)
async def analyze_topic(request: TopicRequest):
    """
    Kicks off the main multi-agent analysis for a new topic.
    (This is a DUMMY response for Week 1)
    """
    print(f"[API] Received topic: {request.topic}")
    
    # Return a hard-coded response to prove the API works
    return ReportResponse(
        executive_summary=f"This is a dummy summary for {request.topic}",
        market_trends=["Dummy Trend 1", "Dummy Trend 2"],
        potential_opportunities=["Dummy Opportunity 1"],
        risk_feasibility_section="Dummy risk analysis."
    )

# --- ENDPOINT 2: User-Controlled Deep Dive ---
@app.post("/deep-dive-query", response_model=DeepDiveResponse)
async def deep_dive_query(request: DeepDiveRequest):
    """
    Runs a RAG query against a specific URL (PDF, etc.)
    (This is a DUMMY response for Week 1)
    """
    print(f"[API] Received deep dive: {request.url} | {request.query}")
    
    # Return a hard-coded response
    return DeepDiveResponse(
        answer=f"This is a dummy answer about '{request.query}' "
               f"from the URL {request.url}"
    )