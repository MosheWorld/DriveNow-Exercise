from abc import ABC, abstractmethod
from typing import Dict, Any

class IMessagePublisher(ABC):
    @abstractmethod
    async def publish_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        pass
