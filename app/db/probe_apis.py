"""
Quick probe script to discover which endpoints work for Habitaclia and Fotocasa on RapidAPI.
Run with: .venv/Scripts/python -m app.db.probe_apis
"""
import asyncio
import httpx
import os
import sys

# Load env vars
from dotenv import load_dotenv
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY") or os.getenv("RAPID_API")

HABITACLIA_HOST = "habitaclia.p.rapidapi.com"
FOTOCASA_HOST = "fotocasa.p.rapidapi.com"

HABITACLIA_ENDPOINTS = [
    "/listproperties",
    "/list",
    "/properties",
    "/search",
    "/v1/search",
    "/v1/list",
    "/v1/properties",
    "/api/properties",
    "/api/list",
]

FOTOCASA_ENDPOINTS = [
    "/listproperties", 
    "/list",
    "/properties",
    "/search",
    "/v1/search",
    "/v1/list",
]

COMMON_PARAMS = {
    "location": "barcelona",
    "operation": "rent",
    "propertyType": "flats",
    "numPage": "1",
}

async def probe_endpoint(client: httpx.AsyncClient, host: str, path: str, key: str) -> dict:
    url = f"https://{host}{path}"
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": host
    }
    try:
        r = await client.get(url, headers=headers, params=COMMON_PARAMS, timeout=10)
        body_preview = r.text[:300].replace("\n", " ")
        return {"url": url, "status": r.status_code, "preview": body_preview}
    except Exception as e:
        return {"url": url, "status": "ERROR", "preview": str(e)}

async def main():
    if not RAPIDAPI_KEY:
        print("ERROR: No RAPIDAPI_KEY found in .env")
        sys.exit(1)
    
    print(f"Using key: {RAPIDAPI_KEY[:8]}...")
    print()

    async with httpx.AsyncClient() as client:
        print("=" * 60)
        print("HABITACLIA PROBE")
        print("=" * 60)
        for path in HABITACLIA_ENDPOINTS:
            result = await probe_endpoint(client, HABITACLIA_HOST, path, RAPIDAPI_KEY)
            status = result["status"]
            marker = "[OK]" if status == 200 else "[--]"
            print(f"{marker} [{status}] {result['url']}")
            if status == 200:
                print(f"   Preview: {result['preview'][:200]}")
            print()
        
        print("=" * 60)
        print("FOTOCASA PROBE")
        print("=" * 60)
        for path in FOTOCASA_ENDPOINTS:
            result = await probe_endpoint(client, FOTOCASA_HOST, path, RAPIDAPI_KEY)
            status = result["status"]
            marker = "[OK]" if status == 200 else "[--]"
            print(f"{marker} [{status}] {result['url']}")
            if status == 200:
                print(f"   Preview: {result['preview'][:200]}")
            print()

if __name__ == "__main__":
    asyncio.run(main())
