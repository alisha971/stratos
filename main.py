# Create this file in the root: insightbridge/main.py

import uvicorn
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "backend.api:app",  # Path to your FastAPI app
        host="0.0.0.0",     # Listen on all network interfaces
        port=8000,          # The port to run on
        reload=True         # Auto-reload the server when code changes
    )