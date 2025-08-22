import os
import httpx
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import Response

app = FastAPI()

VALID_API_KEY = os.getenv("API_KEY")
UPSTREAM_URL = os.getenv("UPSTREAM_URL")

def validate_api_key(x_api_key: str = Header(...)):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
    return x_api_key

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy(path: str, api_key: str = Depends(validate_api_key), request: httpx.Request = None):
    async with httpx.AsyncClient() as client:
        req_method = request.method if request else "GET"
        req_headers = dict(request.headers) if request else {}
        req_content = await request.body() if request else None
        upstream_resp = await client.request(
            req_method,
            f"{UPSTREAM_URL}/{path}",
            headers=req_headers,
            content=req_content,
            params=request.query_params if request else None
        )
    return Response(content=upstream_resp.content, status_code=upstream_resp.status_code, headers=dict(upstream_resp.headers))
