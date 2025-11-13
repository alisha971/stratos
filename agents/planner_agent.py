# stratos/agents/planner_agent.py
"""
PlannerAgent: creates a step-by-step plan of action for research.
It returns a list of PlanStep objects (matching orchestrator.state.PlanStep).
"""

from typing import List, Dict
from orchestrator.state import PlanStep, AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import uuid

# LLM loaded once
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2)

planner_prompt = ChatPromptTemplate.from_template(
    """
    You are PlannerAgent. Given a user topic, produce a concise
    ordered plan (3-6 steps) where each step specifies:
      - a short step_id (no spaces)
      - description
      - tool to use (choose from: tavily_search, gnews, arxiv_search, web_search, pdf_rag_query)
      - the exact query string to run
      - include_images: true/false

    Output MUST be a JSON array of objects with the keys:
    step_id, description, tool, query, include_images

    TOPIC:
    {topic}
    """
)

def run_planner_node(state: AgentState) -> Dict:
    topic = state['topic']
    print(f"\n--- [Node: PlannerAgent] ---")
    print(f"Topic: {topic}")

    chain = planner_prompt | llm
    print("Generating plan...")
    response = chain.invoke({"topic": topic}).content

    # Try to parse JSON. If LLM fails, fall back to a simple deterministic plan.
    import json
    try:
        plan_raw = json.loads(response)
        # Normalize to ensure step_id exists
        plan: List[PlanStep] = []
        for idx, p in enumerate(plan_raw):
            sid = p.get("step_id") or f"step_{idx+1}"
            plan.append({
                "step_id": sid,
                "description": p.get("description", ""),
                "tool": p.get("tool", "tavily_search"),
                "query": p.get("query", topic),
                "include_images": bool(p.get("include_images", False))
            })
    except Exception as e:
        print(f"[PlannerAgent] LLM plan parse failed: {e}\nFalling back to default plan.")
        plan = [
            {"step_id": "tavily_basic", "description": "Search general web articles", "tool": "tavily_search", "query": topic, "include_images": True},
            {"step_id": "gnews", "description": "Fetch recent news", "tool": "gnews", "query": topic, "include_images": False},
            {"step_id": "arxiv", "description": "Find academic papers", "tool": "arxiv_search", "query": f"{topic} review OR survey", "include_images": False}
        ]

    # Return updates to state
    return {
        "plan": plan,
        "iteration_count": state.get("iteration_count", 0)
    }
