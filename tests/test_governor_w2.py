from dotenv import load_dotenv
load_dotenv()
import os
# We import the SINGLETON instance from our new file
from mcp.governor import mcp_governor
import pprint # For nice printing

def run_tests():
    print("--- STARTING WEEK 2 GOVERNOR TESTS ---")
    
    # --- Test 1: A successful call ---
    print("\n--- Test 1: ResearchAgent (Tavily) ---")
    try:
        results = mcp_governor.execute_tool(
            agent_name="ResearchAgent",
            tool_name="tavily_search",
            tool_input="AI in supply chain"
        )
        pprint.pprint(results)
    except Exception as e:
        print(f"TEST FAILED: {e}")

    # --- Test 2: A permission error ---
    print("\n--- Test 2: AnalystAgent (Tavily) - SHOULD FAIL ---")
    try:
        results = mcp_governor.execute_tool(
            agent_name="AnalystAgent",
            tool_name="tavily_search",
            tool_input="AI in supply chain"
        )
        pprint.pprint(results)
    except PermissionError as e:
        print(f"TEST PASSED (Correctly Denied): {e}")
    except Exception as e:
        print(f"TEST FAILED (Wrong Error): {e}")

    # --- Test 3: The complex RAG tool ---
    print("\n--- Test 3: UserDeepDive (PDF RAG) ---")
    try:
        # A well-known, stable PDF link for testing
        test_url = "https://arxiv.org/pdf/1706.03762.pdf" # "Attention Is All You Need"
        test_query = "What is the 'self-attention' mechanism?"
        
        results = mcp_governor.execute_tool(
            agent_name="UserDeepDive",
            tool_name="pdf_rag_query",
            tool_input={
                "url": test_url,
                "query": test_query
            }
        )
        pprint.pprint(results)
    except Exception as e:
        print(f"TEST FAILED: {e}")

    print("\n--- ALL TESTS COMPLETE ---")

if __name__ == "__main__":
    # Make sure your .env file is loaded
    from dotenv import load_dotenv
    load_dotenv()
    
    run_tests()