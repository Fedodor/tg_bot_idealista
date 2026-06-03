"""
Quick probe to find the correct Habitaclia locationId for Barcelona.
Run with: .venv/Scripts/python -m app.db.probe_habitaclia_locations
"""
import asyncio
import httpx
import os
import sys

from dotenv import load_dotenv
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY") or os.getenv("RAPID_API")
HOST = "habitaclia.p.rapidapi.com"

async def main():
    if not RAPIDAPI_KEY:
        print("ERROR: No RAPIDAPI_KEY found in .env")
        sys.exit(1)

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": HOST
    }

    # First, try the locations endpoint
    async with httpx.AsyncClient(timeout=15) as client:
        # Try to find the locations endpoint
        for path in ["/locations", "/v1/locations", "/suggestlocations", "/suggest", "/autocomplete"]:
            url = f"https://{HOST}{path}"
            try:
                r = await client.get(url, headers=headers, params={"text": "barcelona"}, timeout=10)
                print(f"[{r.status_code}] {url}")
                if r.status_code == 200:
                    print(f"   Response: {r.text[:500]}")
            except Exception as e:
                print(f"[ERR] {url}: {e}")
            print()

        # Also try /listproperties with what we know about locationId format
        print("--- Trying /listproperties with different locationId formats ---")
        for loc_id in [
            "listados/viviendas-barcelona",
            "listados/alquiler-pisos-barcelona",
            "listados/alquiler-barcelona",
            "alquiler/pisos/barcelona-provincia/",
            "barcelona",
            "92",  # numeric IDs common in Spanish portals
            "8019",
        ]:
            url = f"https://{HOST}/listproperties"
            try:
                r = await client.get(url, headers=headers, params={
                    "locationId": loc_id, 
                    "numPage": "1",
                    "order": "habitacliascore"
                }, timeout=10)
                print(f"[{r.status_code}] locationId={loc_id!r}")
                if r.status_code == 200:
                    preview = r.text[:400]
                    print(f"   Response: {preview}")
            except Exception as e:
                print(f"[ERR] {e}")
            print()

if __name__ == "__main__":
    asyncio.run(main())
