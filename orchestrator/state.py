# Create this file: insightbridge/orchestrator/state.py

from typing import List, TypedDict

class AgentState(TypedDict):
    """
    This is the "shared memory" for all agents.
    It defines the structure of data that flows through the graph.
    """
    topic: str               # The initial user query
    iteration_count: int     # To prevent infinite loops
    
    # --- Tool Outputs ---
    documents: List[str]     # The list of docs from the ResearchAgent
    
    # --- Agent Outputs ---
    draft_report: str        # The draft from the AnalystAgent
    critique: str            # The critique from the CriticAgent
    
    # --- Final Output ---
    final_report: str        # The final JSON report from the StrategistAgent