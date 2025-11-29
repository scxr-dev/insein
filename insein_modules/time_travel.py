"""
[ INSEIN MODULE - TIME TRAVEL (OSINT) ]
AUTHOR: R H A Ashan Imalka (scxr-dev)

DESCRIPTION:
Performs historical analysis of the target using public archive APIs.
This module queries external databases to identify services that were 
previously running on the target ports but are currently closed or hidden.
"""

import aiohttp
import asyncio
import json
from datetime import datetime

class TimeTraveler:
    def __init__(self, target_domain: str):
        self.target = target_domain
        self.wayback_api = "http://archive.org/wayback/available"

    async def get_history(self) -> dict:
       
        async with aiohttp.ClientSession() as session:
            try:
                params = {"url": self.target}
                async with session.get(self.wayback_api, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_wayback(data)
            except Exception:
                return {"status": "ERROR", "message": "Connection to Archive API failed"}
        
        return {"status": "NO_DATA"}

    def _parse_wayback(self, data: dict) -> dict:
        
        try:
            snapshots = data.get("archived_snapshots", {})
            closest = snapshots.get("closest", {})
            
            if closest and closest.get("available"):
                return {
                    "status": "FOUND",
                    "last_seen": closest.get("timestamp"),
                    "archive_url": closest.get("url"),
                    "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        except Exception:
            pass
            
        return {"status": "NOT_FOUND"}