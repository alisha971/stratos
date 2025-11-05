# Create this file: insightbridge/agents/strategist_agent.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from backend.schema import ReportResponse # Import our Pydantic model
from langchain_core.output_parsers.json import JsonOutputParser
from orchestrator.state import AgentState

# Initialize the LLM (Gemini)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.1)

# Pydantic model to JSON parser
parser = JsonOutputParser(pydantic_object=ReportResponse)

strategist_prompt = ChatPromptTemplate.from_template(
    """
    You are a C-level strategist. Your job is to take a
    final, approved draft report and format it perfectly into
    the required JSON output.
    
    You must extract the key points for each section and present them
    as lists of strings.
    
    {format_instructions}
    
    APPROVED DRAFT REPORT:
    {approved_draft}
    """
)

def run_strategist_node(state: AgentState) -> dict:
    """
    This node takes the final approved draft and formats
    it into the required JSON output.
    """
    print(f"\n--- [Node: StrategistAgent] ---")
    draft_report = state['draft_report']
    
    # Get the format instructions from the parser
    format_instructions = parser.get_format_instructions()
    
    # Create the chain
    chain = strategist_prompt | llm | parser
    
    print("Formatting final report...")
    final_report = chain.invoke({
        "approved_draft": draft_report,
        "format_instructions": format_instructions
    })
    
    # The 'final_report' is now a Python dictionary
    # We'll store it as a string in the state for consistency
    import json
    final_report_json = json.dumps(final_report)
    
    print("Final report JSON generated.")
    
    return {
        "final_report": final_report_json
    }