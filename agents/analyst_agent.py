# stratos/agents/analyst_agent.py

import json
import re
from orchestrator.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Initialize LLM (pass API key via env or your standard loader elsewhere)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.7)

# Prompt: escaped JSON schema + clear instruction to output JSON only.
analyst_prompt = ChatPromptTemplate.from_template(
    """
    You are a world-class business analyst. You will produce a structured JSON
    report based ONLY on the research documents provided.

    Input:
    DOCUMENTS: {documents}

    Requirements:
    - Produce a JSON object EXACTLY in this structure (no extra text outside JSON):

      {{
        "title": "string",
        "executive_summary": "string",
        "market_trends": [
          {{
            "point": "string",
            "citations": ["doc_id1", "doc_id2"]
          }}
        ],
        "opportunities": [
          {{
            "opportunity": "string",
            "impact": "string",
            "citations": ["doc_id"]
          }}
        ],
        "risks": [
          {{
            "risk": "string",
            "likelihood": "string",
            "citations": ["doc_id"]
          }}
        ],
        "comparison_table_markdown": "string",
        "image_references": [
          {{
            "id": "image_id",
            "caption": "caption text",
            "url": "image_url"
          }}
        ],
        "recommendations": ["string"],
        "metadata": {{
          "doc_count": 0
        }}
      }}

    - Use ONLY the facts from DOCUMENTS.
    - If DOCUMENTS is empty, produce a JSON with empty lists/strings and metadata.doc_count = 0.
    - Output MUST be valid JSON. NO commentary, NO markdown, NO code fences.
    """
)


def _clean_model_output(raw_text: str) -> str:
    """
    Clean the model output before JSON parsing:
    - Remove triple-backticks and optional '```json' fences
    - Strip leading/trailing whitespace and any pre/post text
    - Attempt to extract the first {...} JSON object if present
    """
    if not isinstance(raw_text, str):
        return ""

    text = raw_text.strip()

    # remove common code fences
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text, flags=re.IGNORECASE)

    # If the model prefaced the JSON with text, try to extract the {...} block
    match = re.search(r"(\{[\s\S]*\})", text)
    if match:
        candidate = match.group(1)
        return candidate.strip()

    return text


def run_analyst_node(state: AgentState) -> dict:
    print(f"\n--- [Node: AnalystAgent] ---")
    documents = state.get("documents", [])
    docs_json = json.dumps(documents, ensure_ascii=False)

    chain = analyst_prompt | llm

    print("Generating draft structured report (JSON)...")
    try:
        response = chain.invoke({"documents": docs_json}).content
    except Exception as e:
        # On LLM errors (including rate limits), produce a safe fallback template
        print(f"[AnalystAgent] LLM call failed: {e}")
        fallback = {
            "title": f"Analysis for {state.get('topic', '')}",
            "executive_summary": "",
            "market_trends": [],
            "opportunities": [],
            "risks": [],
            "comparison_table_markdown": "",
            "image_references": [],
            "recommendations": [],
            "metadata": {"doc_count": len(documents)}
        }
        return {"draft_report": json.dumps(fallback)}

    cleaned = _clean_model_output(response)

    # Try parsing JSON
    try:
        parsed = json.loads(cleaned)
        # Ensure minimal schema exists
        minimal = {
            "title": parsed.get("title", ""),
            "executive_summary": parsed.get("executive_summary", ""),
            "market_trends": parsed.get("market_trends", []),
            "opportunities": parsed.get("opportunities", []),
            "risks": parsed.get("risks", []),
            "comparison_table_markdown": parsed.get("comparison_table_markdown", ""),
            "image_references": parsed.get("image_references", []),
            "recommendations": parsed.get("recommendations", []),
            "metadata": parsed.get("metadata", {"doc_count": len(documents)})
        }
        draft_report_str = json.dumps(minimal)
    except Exception as e:
        # Parsing failed: return a safe fallback that the Critic can consume
        print(f"[AnalystAgent] JSON parse failed: {e}")
        print(f"[AnalystAgent] Raw model output: {response}")
        fallback = {
            "title": f"Analysis for {state.get('topic', '')}",
            "executive_summary": "",
            "market_trends": [],
            "opportunities": [],
            "risks": [],
            "comparison_table_markdown": "",
            "image_references": [],
            "recommendations": [],
            "metadata": {"doc_count": len(documents)}
        }
        draft_report_str = json.dumps(fallback)

    return {"draft_report": draft_report_str}
