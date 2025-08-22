import os
import httpx
from fastapi import FastAPI, Header, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
import uvicorn

app = FastAPI()

VALID_API_KEY = os.environ["API_KEY"]
UPSTREAM_URL = os.environ["UPSTREAM_URL"]

def validate_api_key(x_api_key: str = Header(...)):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
    return x_api_key

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy(path: str, request: Request, api_key: str = Depends(validate_api_key)):
    headers = dict(request.headers)
    body = await request.body()

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            request.method,
            f"{UPSTREAM_URL}/{path}",
            headers=headers,
            content=body,
            params=request.query_params
        ) as upstream_resp:

            async def stream_generator():
                async for chunk in upstream_resp.aiter_bytes():
                    yield chunk

            return StreamingResponse(
                stream_generator(),
                status_code=upstream_resp.status_code,
                headers=dict(upstream_resp.headers),
                media_type=upstream_resp.headers.get("content-type")
            )

if __name__ == "__main__":
    port = int(os.environ["PORT"])
    uvicorn.run(app, host="0.0.0.0", port=port)
