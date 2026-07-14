from abc import ABC, abstractmethod
from typing import Any, Dict

from app.tools.schemas.tool_models import ToolResponse


class BaseTool(ABC):
    """
    Abstract base class for all AI tools.
    Every tool in the system must inherit from this class.
    """

    # Unique tool name used by the AI
    name: str

    # Description used by the LLM to decide when to call the tool
    description: str

    # Tool risk level (0, 1, or 2)
    tier: int

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResponse:
        """
        Execute the tool.

        Returns:
            ToolResponse
        """
        pass

    def metadata(self) -> Dict[str, Any]:
        """
        Information exposed to the LLM.
        """
        return {
            "name": self.name,
            "description": self.description,
            "tier": self.tier,
        }