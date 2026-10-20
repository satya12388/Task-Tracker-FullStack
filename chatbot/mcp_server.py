from Backend.app import app
from fastapi_mcp import FastApiMCP
mcp = FastApiMCP(app)
mcp.mount()
