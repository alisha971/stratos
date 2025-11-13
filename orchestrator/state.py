# Create this file: insightbridge/orchestrator/state.py

from typing import List, TypedDict, Dict, Any

class Citation(TypedDict):
    id: str
    title: str
    url: str
    summary: str
    source: str
    score: float
    images: List[str]

class PlanStep(TypedDict):
    step_id: str
    description: str
    tool: str          # e.g. "tavily_search" or "arxiv_search"
    query: str
    include_images: bool

class AgentState(TypedDict):
    """
    This is the "shared memory" for all agents.
    It defines the structure of data that flows through the graph.
    """
    # Input
    topic: str               # The initial user query
    iteration_count: int     # To prevent infinite loops
    
    # Planner output
    plan: List[PlanStep]  # ordered plan steps

    # --- Tool Outputs ---
    # Research outputs (list of citation objects)
    documents: List[Citation]
    
    # --- Agent Outputs ---
    draft_report: str        # The draft from the AnalystAgent
    critique: str            # The critique from the CriticAgent
    
    # --- Final Output ---
    final_report: str        # The final JSON report from the StrategistAgent