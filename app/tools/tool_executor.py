from typing import Any

from app.tools.schemas.tool_models import ToolResponse
from app.tools.tool_registry import ToolRegistry


class ToolExecutor:
    """
    Executes tools registered in the ToolRegistry.
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    async def execute(self, tool_name: str, **kwargs: Any) -> ToolResponse:
        """
        Execute a tool by its name.
        """

        tool = self.registry.get(tool_name)

        if tool is None:
            return ToolResponse(
                success=False,
                message=f"Tool '{tool_name}' not found.",
                data=None
            )

        return await tool.execute(**kwargs)