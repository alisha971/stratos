# Edit this file: insightbridge/backend/api.py
# (We are modifying the /analyze-topic endpoint)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from fastapi import FastAPI, HTTPException
from .schema import (
    TopicRequest, 
    ReportResponse, 
    DeepDiveRequest, 
    DeepDiveResponse
)
# --- Import our compiled graph AND our governor ---
from orchestrator.graph_builder import app_graph
from mcp.governor import mcp_governor
import json

app = FastAPI(
    title="InsightBridge API",
    description="Agentic AI for business research and deep-dive analysis."
)

# --- ENDPOINT 1: Main Report Generation (NOW REAL) ---
@app.post("/analyze-topic", response_model=ReportResponse)
async def analyze_topic(request: TopicRequest):
    """
    Kicks off the main multi-agent analysis for a new topic.
    """
    print(f"\n[API] Received topic: {request.topic}")
    
    # This is the input for our graph
    initial_state = {
        "topic": request.topic,
        "iteration_count": 0
    }
    
    try:
        # Run the graph!
        # .invoke() is synchronous. For a production app,
        # you'd use .ainvoke() and run it in the background.
        final_state = app_graph.invoke(initial_state)
        
        # Get the final report JSON string from the state
        report_json = final_state.get("final_report")
        
        if not report_json:
            raise HTTPException(status_code=500, detail="Report generation failed.")

        # Convert the JSON string back into a dictionary
        report_data = json.loads(report_json)
        
        # Validate and return the Pydantic model
        return ReportResponse(**report_data)

    except Exception as e:
        print(f"[API] Error during graph invocation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINT 2: User-Controlled Deep Dive (Stays the same) ---
@app.post("/deep-dive-query", response_model=DeepDiveResponse)
async def deep_dive_query(request: DeepDiveRequest):
    """
    Runs a RAG query against a specific URL (PDF, etc.)
    (This code is from Week 2 and is already functional)
    """
    print(f"\n[API] Received deep dive: {request.url} | {request.query}")
    try:
        result_snippets = mcp_governor.execute_tool(
            agent_name="UserDeepDive",
            tool_name="pdf_rag_query",
            tool_input={'url': request.url, 'query': request.query}
        )
        
        # --- SIMPLE IMPROVEMENT ---
        # Let's use an LLM to synthesize the snippets
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")
        prompt = ChatPromptTemplate.from_template(
            "Answer the user's question based *only* on the following context:\n"
            "CONTEXT:\n{context}\n\n"
            "QUESTION:\n{question}"
        )
        chain = prompt | llm
        answer = chain.invoke({
            "context": result_snippets,
            "question": request.query
        }).content

        return DeepDiveResponse(answer=answer)

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))