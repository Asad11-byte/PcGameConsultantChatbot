import json
from pathlib import Path

from app.tools.core.base_tool import BaseTool
from app.tools.schemas.tool_models import ToolResponse


class PCBuilderTool(BaseTool):

    name = "pc_builder"

    description = (
        "Recommend a gaming PC build based on the user's budget and purpose."
    )

    tier = 0

    def __init__(self):
        self.database = self.load_database()

    def load_database(self):
        database_path = (
            Path(__file__).parent.parent / "data" / "pc_builds.json"
        )
        with open(database_path, "r", encoding="utf-8") as file:
            return json.load(file)

    async def execute(
        self,
        budget: str,
        purpose: str
    ) -> ToolResponse:

        try:
            build = self.database[budget][purpose]

            return ToolResponse(
                success=True,
                message="PC build generated successfully.",
                data=build
            )

        except KeyError:
            return ToolResponse(
                success=False,
                message="No PC build found for the given budget and purpose.",
                data=None
            )