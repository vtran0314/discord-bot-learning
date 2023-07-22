from typing import Protocol

class Messenger(Protocol):
    async def send_message(self, message: str):
        ...