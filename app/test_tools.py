import asyncio
from unittest import result

from app.tools.tool_registry import ToolRegistry
from app.tools.tool_executor import ToolExecutor


async def main():
    registry = ToolRegistry()
    executor = ToolExecutor(registry)

    result = await executor.execute(
    tool_name="pc_builder",
    budget="1000",
    purpose="Gaming"
)

    print(result.model_dump())


if __name__ == "__main__":
    asyncio.run(main())