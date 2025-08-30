from mcp_server.fast_mcp import mcp

# Exponer el servidor como una app ASGI para uvicorn
app = mcp.streamable_http_app
