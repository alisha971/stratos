# Create this file: insightbridge/agents/analyst_agent.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from orchestrator.state import AgentState

# Initialize the LLM (Gemini)
# This is loaded once when the app starts
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.7)

analyst_prompt = ChatPromptTemplate.from_template(
    """
    You are a world-class business analyst. Your job is to analyze the
    provided research documents and synthesize them into a draft report.

    Focus on identifying key market trends, potential opportunities, and
    significant risks. Use clear, professional language.

    RESEARCH DOCUMENTS:
    {documents}
    
    ---
    Produce a draft report with the following sections:
    - Executive Summary
    - Market Trends
    - Potential Opportunities
    - Risk & Feasibility
    """
)

def run_analyst_node(state: AgentState) -> dict:
    """
    This node runs the analysis and generates a draft report.
    """
    print(f"\n--- [Node: AnalystAgent] ---")
    documents = state['documents']
    
    # Format the documents for the prompt
    doc_string = "\n\n---\n\n".join(documents)
    
    # Create the chain
    chain = analyst_prompt | llm
    
    print("Generating draft report...")
    draft_report = chain.invoke({"documents": doc_string}).content
    
    print("Draft report generated.")
    
    return {
        "draft_report": draft_report
    }