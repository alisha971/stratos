# Create this file: insightbridge/backend/schema.py

from pydantic import BaseModel
from typing import List, Optional

class TopicRequest(BaseModel):
    """The input request for the main analysis report."""
    topic: str

class ReportResponse(BaseModel):
    """The final structured output for the main report."""
    executive_summary: str
    market_trends: List[str]
    potential_opportunities: List[str]
    risk_feasibility_section: str

class DeepDiveRequest(BaseModel):
    """The input for the user's follow-up PDF query."""
    url: str    # The PDF or source URL
    query: str  # The specific question
    
class DeepDiveResponse(BaseModel):
    """The answer from the deep-dive RAG query."""
    answer: str