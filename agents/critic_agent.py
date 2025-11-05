# Create this file: insightbridge/agents/critic_agent.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from orchestrator.state import AgentState

# Initialize the LLM (Gemini)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.0)

critic_prompt = ChatPromptTemplate.from_template(
    """
    You are a meticulous and demanding editor. Your job is to review
    the following draft report.

    Your ONLY goal is to check for quality and depth.
    - If the report is high-quality, detailed, and insightful,
      respond ONLY with the word "APPROVED".
    - If the report is shallow, vague, or misses key details,
      respond with a concise, 1-2 sentence critique of *what is missing*.
      (e.g., "The risk section is too generic. It needs to
       identify specific market competitors.")
    
    DRAFT REPORT:
    {draft_report}
    """
)

def run_critic_node(state: AgentState) -> dict:
    """
    This node runs the critique and decides if the report is good enough.
    """
    print(f"\n--- [Node: CriticAgent] ---")
    draft_report = state['draft_report']
    
    # Create the chain
    chain = critic_prompt | llm
    
    print("Critiquing draft report...")
    critique = chain.invoke({"draft_report": draft_report}).content
    
    print(f"Critique: {critique}")
    
    return {
        "critique": critique
    }