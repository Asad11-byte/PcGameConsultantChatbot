import json
from pathlib import Path

from app.tools.core.base_tool import BaseTool
from app.tools.schemas.tool_models import ToolResponse


class FPSEstimatorTool(BaseTool):

    name = "fps_estimator"

    description = (
        "Estimate average FPS for a game based on CPU, GPU, RAM, "
        "resolution and graphics settings."
    )

    tier = 0

    # Load the database once when the tool is created
    def __init__(self):
        self.database = self.load_database()

    def load_database(self):
        database_path = (
            Path(__file__).parent.parent / "data" / "fps_database.json"
        )

        with open(database_path, "r", encoding="utf-8") as file:
            return json.load(file)

    async def execute(
        self,
        cpu: str,
        gpu: str,
        ram: int,
        game: str,
        resolution: str,
        settings: str
    ) -> ToolResponse:

        try:
            estimated_fps = self.database[game][gpu][resolution][settings]

            return ToolResponse(
                success=True,
                message="FPS estimated successfully.",
                data={
                    "cpu": cpu,
                    "gpu": gpu,
                    "ram": ram,
                    "game": game,
                    "resolution": resolution,
                    "settings": settings,
                    "estimated_fps": estimated_fps
                }
            )

        except KeyError:
            return ToolResponse(
                success=False,
                message="Benchmark data not found.",
                data=None
            )