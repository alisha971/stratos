# Create this file: insightbridge/mcp/governor.py

import yaml
from dotenv import load_dotenv

# --- Import ALL your adapter functions ---
from .adapters.tavily_adapter import tavily_search
from .adapters.arxiv_adapter import arxiv_search
from .adapters.web_adapter import read_webpage
from .adapters.news_adapter import gnews
from .adapters.pdf_rag_adapter import pdf_rag_query

# Load .env variables (like GOOGLE_API_KEY)
load_dotenv()

class MCPGovernor:
    def __init__(self, config_path="mcp/config.yml"):
        """
        Initializes the Governor by loading the rulebook and mapping tools.
        """
        print("\n--- MCP Governor Initializing ---")
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        print("Config 'rulebook' loaded.")

        # This 'toolbox' maps the tool NAMES from the config
        # to the actual Python FUNCTIONS you imported.
        self.toolbox = {
            "tavily_search": tavily_search,
            "arxiv_search": arxiv_search,
            "read_webpage": read_webpage,
            "gnews": gnews,
            "pdf_rag_query": pdf_rag_query
        }
        print(f"All {len(self.toolbox)} tools registered in toolbox.")
        print("--- MCP Governor Ready ---\n")

    def execute_tool(self, agent_name: str, tool_name: str, tool_input: any):
        """
        The main "firewall" function.
        An agent MUST call this to use any tool.
        """
        print(f"[MCP-FIREWALL] Request from '{agent_name}' to use tool '{tool_name}'")

        # 1. PERMISSION CHECK: Does this agent exist in the config?
        agent_rules = self.config['agents'].get(agent_name)
        if not agent_rules:
            print(f"[MCP-FIREWALL] DENIED: Agent '{agent_name}' not found in config.")
            raise PermissionError(f"Agent '{agent_name}' not found in config.")

        # 2. PERMISSION CHECK: Is this tool in the agent's "allowed_tools" list?
        if tool_name not in agent_rules['allowed_tools']:
            print(f"[MCP-FIREWALL] DENIED: '{agent_name}' is NOT allowed to use '{tool_name}'.")
            raise PermissionError(f"'{agent_name}' is not allowed to use '{tool_name}'.")
        
        # 3. TOOL CHECK: Does this tool exist in our toolbox?
        tool_function = self.toolbox.get(tool_name)
        if not tool_function:
            print(f"[MCP-FIREWALL] DENIED: Tool '{tool_name}' not implemented in governor.")
            raise NotImplementedError(f"Tool '{tool_name}' not implemented.")

        # 4. PASSED! Execute the tool.
        print(f"[MCP-FIREWALL] GRANTED: Executing '{tool_name}'.")
        try:
            # This logic smartly handles both simple and complex tools
            if isinstance(tool_input, dict):
                # For pdf_rag_query(url=..., query=...)
                result = tool_function(**tool_input)
            else:
                # For tavily_search(query), gnews(query), etc.
                result = tool_function(tool_input)
                
            return result
        except Exception as e:
            print(f"[MCP-FIREWALL] FAILED: Tool '{tool_name}' failed during execution.")
            print(f"Error: {e}")
            return f"Error executing tool {tool_name}: {e}"

# --- SINGLETON INSTANCE ---
# We create one, and only one, instance of the Governor
# when the app starts. All other files will import this.
mcp_governor = MCPGovernor()