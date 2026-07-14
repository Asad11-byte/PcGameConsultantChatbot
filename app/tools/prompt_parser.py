import re


class PromptParser:

    @staticmethod
    def extract_fps_parameters(prompt: str):

        prompt_lower = prompt.lower()

        cpu = None
        gpu = None
        ram = None
        game = None
        resolution = None
        settings = None

        # CPU
        cpu_match = re.search(
            r"(ryzen\s\d\s\d{4}|i[3579]-\d{4,5}[a-z]?)",
            prompt,
            re.IGNORECASE
        )

        if cpu_match:
            cpu = cpu_match.group(0)

        # GPU
        gpu_match = re.search(
            r"(RTX\s\d{4}|GTX\s\d{3,4}|RX\s\d{4})",
            prompt,
            re.IGNORECASE
        )

        if gpu_match:
            gpu = gpu_match.group(0).upper()

        # RAM
        ram_match = re.search(
            r"(\d+)\s?GB",
            prompt,
            re.IGNORECASE
        )

        if ram_match:
            ram = int(ram_match.group(1))

        # Resolution
        for value in ["1080p", "1440p", "4k"]:
            if value.lower() in prompt_lower:
                resolution = value
                break

        # Graphics Settings
        for value in ["Low", "Medium", "High", "Ultra"]:
            if value.lower() in prompt_lower:
                settings = value
                break

        # Game
        games = [
            "Cyberpunk 2077",
            "GTA V"
        ]

        for g in games:
            if g.lower() in prompt_lower:
                game = g
                break

        return {
            "cpu": cpu,
            "gpu": gpu,
            "ram": ram,
            "game": game,
            "resolution": resolution,
            "settings": settings
        }

    @staticmethod
    def extract_pc_build_parameters(prompt: str):

        budget = None
        purpose = "Gaming"

        budget_match = re.search(r"\$?(\d{3,5})", prompt)

        if budget_match:
            budget = budget_match.group(1)

        return {
            "budget": budget,
            "purpose": purpose
        }