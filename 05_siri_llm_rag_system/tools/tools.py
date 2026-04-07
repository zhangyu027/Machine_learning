from __future__ import annotations
from datetime import datetime

def get_current_time() -> str:
    return datetime.utcnow().isoformat() + "Z"

def maybe_use_tools(query: str) -> dict:
    used = []
    tool_outputs = []
    q = query.lower()
    if "time" in q or "current time" in q:
        used.append("get_current_time")
        tool_outputs.append(f"Current UTC time: {get_current_time()}")
    return {"used_tools": used, "tool_outputs": tool_outputs}