from pydantic import BaseModel
from typing import Dict, Any
from common.messaging.messaging_constants import KEY_EVENT_TYPE, KEY_PAYLOAD
import json

class MessageEvent(BaseModel):
    event_type: str
    payload: Dict[str, Any]

    def to_json(self) -> str:
        return self.model_dump_json()
