# stratos/backend/api.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import asyncio

# Import the compiled graph and planner helper
from orchestrator.graph_builder import app_graph
from agents.planner_agent import run_planner_node
from orchestrator.state import AgentState

app = FastAPI(
    title="Stratos Insight API",
    description="Agentic AI for research and analysis (Stratos).",
)

# --- CORS (critical for Next.js frontend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas (simplified; adapt to your schema.py)
class TopicRequest(BaseModel):
    topic: str

class ReportResponse(BaseModel):
    title: str
    executive_summary: str
    market_trends: list
    opportunities: list
    risks: list
    comparison_table_markdown: str
    image_references: list
    recommendations: list
    metadata: dict

# --- Endpoint 1: synchronous (unchanged-ish) ---
@app.post("/analyze-topic", response_model=ReportResponse)
async def analyze_topic(request: TopicRequest):
    print(f"\n[API] Received topic: {request.topic}")
    initial_state = {
        "topic": request.topic,
        "iteration_count": 0
    }
    try:
        final_state = app_graph.invoke(initial_state)
        report_json = final_state.get("final_report") or final_state.get("draft_report")
        if not report_json:
            raise HTTPException(status_code=500, detail="Report generation failed.")
        report_data = json.loads(report_json) if isinstance(report_json, str) else report_json
        return ReportResponse(**report_data)
    except Exception as e:
        print(f"[API] Error during graph invocation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoint 2: Streaming SSE for UI to show Plan + final report ---
@app.post("/analyze-topic-stream")
async def analyze_topic_stream(request: Request):
    """
    Server-Sent Events endpoint. It will:
      1) Run the planner node and stream the plan
      2) Run the full graph synchronously and stream the final report
    """
    body = await request.json()
    topic = body.get("topic")
    if not topic:
        raise HTTPException(status_code=400, detail="Missing topic")

    initial_state: AgentState = {
        "topic": topic,
        "iteration_count": 0
    }

    async def event_generator():
        # 1) Run planner node directly to get plan (quick)
        try:
            planner_update = run_planner_node(initial_state)
            plan = planner_update.get("plan", [])
            event = {"type": "plan", "payload": plan}
            yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            err = {"type": "error", "payload": f"Planner failed: {e}"}
            yield f"data: {json.dumps(err)}\n\n"
            return

        # 2) Now run the full graph (blocking). We yield a "working" event first.
        yield f"data: {json.dumps({'type': 'status', 'payload': 'running_graph'})}\n\n"

        loop = asyncio.get_event_loop()
        try:
            # Running a synchronous graph in async endpoint: run in executor
            final_state = await loop.run_in_executor(None, lambda: app_graph.invoke({
                "topic": topic,
                "iteration_count": 0,
                "plan": plan
            }))
            # get draft or final report
            report_json = final_state.get("final_report") or final_state.get("draft_report")
            if not report_json:
                raise Exception("Report generation failed (no output).")
            # Ensure it's JSON serializable
            report_obj = json.loads(report_json) if isinstance(report_json, str) else report_json
            yield f"data: {json.dumps({'type': 'report', 'payload': report_obj})}\n\n"
            # Finished
            yield f"data: {json.dumps({'type': 'status', 'payload': 'complete'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'payload': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
