import aiohttp
import asyncio
import json
from datetime import datetime

API_URL = "https://www.federalregister.gov/api/v1/documents.json"
OUTPUT_FILE = "raw_documents.json"

async def fetch_documents():
    params = {
        "date_from": "2025-01-01",
        "date_to": datetime.today().strftime('%Y-%m-%d'),
        "per_page": 100,
        "page": 1
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                with open(OUTPUT_FILE, 'w') as f:
                    json.dump(data, f, indent=4)
                print(f"Fetched {len(data['results'])} documents in {OUTPUT_FILE}.")
            else:
                print(f"Failed to fetch Records: {response.status}")

if __name__ == "__main__":
    asyncio.run(fetch_documents())
