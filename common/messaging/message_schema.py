from pydantic import BaseModel
from typing import Dict, Any

class MessageEvent(BaseModel):
    event_type: str
    payload: Dict[str, Any]

    def to_json(self) -> str:
        return self.model_dump_json()
