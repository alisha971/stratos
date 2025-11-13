# stratos/orchestrator/graph_builder.py

from langgraph.graph import StateGraph, END
from .state import AgentState

# Import node functions
from agents.planner_agent import run_planner_node
from agents.research_agent import run_researcher_node
from agents.analyst_agent import run_analyst_node
from agents.critic_agent import run_critic_node
from agents.strategist_agent import run_strategist_node

# --- 1. Define the Conditional Edge Logic ---
def should_continue(state: AgentState) -> str:
    """
    Critic decision point. If critique contains APPROVED OR max iterations reached,
    move to strategist; otherwise, return to researcher. For Option C we only allow
    one retry (iteration_count > 1).
    """
    print(f"\n--- [Edge: should_continue] ---")
    critique = state.get('critique', "") or ""
    iteration_count = state.get('iteration_count', 0)

    MAX_ITER = 1  # Option C: allow ONLY one retry

    if iteration_count > MAX_ITER:
        print("Max iterations reached. Moving to strategist.")
        return "end_critique_loop"

    if "APPROVED" in critique.upper():
        print("Critique approved. Moving to strategist.")
        return "end_critique_loop"
    else:
        print("Critique found issues. Returning to researcher.")
        return "revise"

# --- 2. Build the Graph ---
print("--- Compiling Stratos Graph ---")
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("planner", run_planner_node)
graph.add_node("researcher", run_researcher_node)
graph.add_node("analyst", run_analyst_node)
graph.add_node("critic", run_critic_node)
graph.add_node("strategist", run_strategist_node)

# Entry point
graph.set_entry_point("planner")

# Standard edges
graph.add_edge("planner", "researcher")
graph.add_edge("researcher", "analyst")
graph.add_edge("analyst", "critic")
graph.add_edge("strategist", END)

# Conditional A2A loop with limited retries
graph.add_conditional_edges(
    "critic",
    should_continue,
    {
        "revise": "researcher",
        "end_critique_loop": "strategist"
    }
)

# Compile the final app_graph
app_graph = graph.compile()
print("--- Graph Compilation Complete ---")
