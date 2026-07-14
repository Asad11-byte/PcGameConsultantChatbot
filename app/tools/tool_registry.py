from typing import Dict, List

from app.tools.core.base_tool import BaseTool
from app.tools.tier0.fps_estimator import FPSEstimatorTool
from app.tools.tier0.pc_builder import PCBuilderTool

class ToolRegistry:

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

        # Register tools here
        self.register(FPSEstimatorTool())
        self.register(PCBuilderTool())
        
    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool

    def get(self, tool_name: str):
        return self._tools.get(tool_name)

    def list_tools(self):
        return [tool.metadata() for tool in self._tools.values()]