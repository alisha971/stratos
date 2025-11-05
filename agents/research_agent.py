# Create this file: insightbridge/agents/research_agent.py

from mcp.governor import mcp_governor # Import the singleton governor
from orchestrator.state import AgentState

def run_researcher_node(state: AgentState) -> dict:
    """
    This node runs the research phase.
    It uses the MCPGovernor to call all its tools.
    """
    topic = state['topic']
    print(f"\n--- [Node: ResearchAgent] ---")
    print(f"Topic: {topic}")

    # Call all the tools via the governor
    # We are allowed to do this because our config.yml
    # gives 'ResearchAgent' permission.
    tavily_results = mcp_governor.execute_tool(
        "ResearchAgent", "tavily_search", topic
    )
    gnews_results = mcp_governor.execute_tool(
        "ResearchAgent", "gnews", topic
    )
    arxiv_results = mcp_governor.execute_tool(
        "ResearchAgent", "arxiv_search", topic
    )
    
    # Combine all results into one list
    all_documents = tavily_results + gnews_results + arxiv_results
    
    print(f"Found {len(all_documents)} documents.")
    
    # Return the *change* to the state
    return {
        "documents": all_documents,
        "iteration_count": state.get('iteration_count', 0) + 1
    }