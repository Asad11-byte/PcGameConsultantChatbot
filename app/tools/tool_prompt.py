TOOL_PROMPT = """
You have access to the following tools.

1. fps_estimator
Description:
Estimate FPS based on CPU, GPU, RAM, game, resolution, and graphics settings.

Required Parameters:
- cpu
- gpu
- ram
- game
- resolution
- settings

2. pc_builder

Description:
Recommend a gaming PC build.

Required Parameters:
- budget
- purpose

If a tool is required, respond ONLY in JSON.

Example:

{
    "tool": "fps_estimator",
    "parameters": {
        "cpu": "Ryzen 5 5600",
        "gpu": "RTX 3060",
        "ram": 16,
        "game": "Cyberpunk 2077",
        "resolution": "1080p",
        "settings": "Ultra"
    }
}

If no tool is required, respond:

{
    "tool": null
}
"""