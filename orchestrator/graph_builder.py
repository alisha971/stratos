# Create this file: insightbridge/orchestrator/graph_builder.py

from langgraph.graph import StateGraph, END
from .state import AgentState

# Import all our agent node functions
from agents.research_agent import run_researcher_node
from agents.analyst_agent import run_analyst_node
from agents.critic_agent import run_critic_node
from agents.strategist_agent import run_strategist_node

# --- 1. Define the Conditional Edge Logic ---
def should_continue(state: AgentState) -> str:
    """
    This is the "Critic's" decision point.
    Based on the critique, it decides to loop back or move on.
    """
    print(f"\n--- [Edge: should_continue] ---")
    critique = state['critique']
    iteration_count = state['iteration_count']

    if iteration_count > 3:
        print("Max iterations reached. Moving to strategist.")
        return "end_critique_loop"
    
    if "APPROVED" in critique:
        print("Critique approved. Moving to strategist.")
        return "end_critique_loop"
    else:
        print("Critique found issues. Returning to researcher.")
        return "revise"

# --- 2. Build the Graph ---
print("--- Compiling InsightBridge Graph ---")
graph = StateGraph(AgentState)

# Add all the nodes
graph.add_node("researcher", run_researcher_node)
graph.add_node("analyst", run_analyst_node)
graph.add_node("critic", run_critic_node)
graph.add_node("strategist", run_strategist_node)

# Set the entry point
graph.set_entry_point("researcher")

# Add the standard edges
graph.add_edge("researcher", "analyst")
graph.add_edge("analyst", "critic")
graph.add_edge("strategist", END)

# Add the *conditional* edge (the A2A loop)
graph.add_conditional_edges(
    "critic",         # Start node
    should_continue,  # Decision function
    {
        "revise": "researcher",       # If "revise", go back to researcher
        "end_critique_loop": "strategist" # If "approve", go to strategist
    }
)

# --- 3. Compile the Graph ---
# This is the final, runnable application
app_graph = graph.compile()
print("--- Graph Compilation Complete ---")