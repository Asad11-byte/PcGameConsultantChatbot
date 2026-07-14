from pyexpat.errors import messages

from app.tools.prompt_parser import PromptParser 

from prompt_toolkit import prompt

from app.tools.tool_registry import ToolRegistry
from app.tools.tool_executor import ToolExecutor

import os

from groq import AsyncGroq
from dotenv import load_dotenv


load_dotenv()


class GroqService:

    def __init__(self, db_service):

        self.client = AsyncGroq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.db_service = db_service

        self.model = "llama-3.3-70b-versatile"
        self.registry = ToolRegistry()
        self.executor = ToolExecutor(self.registry)

    async def process_tools(self, prompt: str):

     prompt_lower = prompt.lower()

    # -------------------------
    # FPS Tool
    # -------------------------

     if "fps" in prompt_lower or "frame rate" in prompt_lower:

        params = PromptParser.extract_fps_parameters(prompt)

        required = [
            "gpu",
            "game",
            "resolution",
            "settings"
        ]

        missing = [
            field
            for field in required
            if not params.get(field)
        ]

        if missing:

            return {
                "missing": True,
                "tool": "fps_estimator",
                "fields": missing
            }

        return await self.executor.execute(
            tool_name="fps_estimator",
            **params
        )

    # -------------------------
    # PC Builder
    # -------------------------

     if (
        "pc build" in prompt_lower
        or "recommend pc" in prompt_lower
        or "build me a pc" in prompt_lower
    ):

        params = PromptParser.extract_pc_build_parameters(prompt)

        if not params.get("budget"):

            return {
                "missing": True,
                "tool": "pc_builder",
                "fields": ["budget"]
            }

        return await self.executor.execute(
            tool_name="pc_builder",
            **params
        )

        return None

    async def get_chat_stream(
        self,
        prompt: str,
        session_id: int
    ):

        try:

            # -------------------------
            # Load previous conversation
            # -------------------------

            history = self.db_service.get_messages(
                session_id
            )

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are AI Gaming Assistant, an expert PC hardware consultant, gaming performance specialist, and computer technician.\n\n"

                        "## Primary Responsibilities\n"
                        "- Diagnose PC hardware and software issues.\n"
                        "- Recommend balanced gaming PC builds for any budget.\n"
                        "- Troubleshoot crashes, BSODs, overheating, driver conflicts, and hardware compatibility.\n"
                        "- Optimize FPS, graphics settings, and overall gaming performance.\n"
                        "- Compare CPUs, GPUs, RAM, SSDs, motherboards, power supplies, and peripherals.\n"
                        "- Explain technical concepts in a simple and beginner-friendly manner.\n"
                        "- Recommend upgrades based on the user's current hardware and gaming goals.\n\n"
                        "## Tool Usage\n"
                        "- Backend tools may provide trusted structured data.\n"
                        "- Always use backend tool results as the primary source of truth.\n"
                        "- Do not change, guess, or invent values returned by tools.\n"
                        "- Explain tool results clearly using Markdown headings and bullet points.\n"
                        "- If a tool reports an error, explain the issue and ask the user for the missing information."

                        "## Response Style\n"
                        "- ALWAYS use Markdown formatting.\n"
                        "- ALWAYS organize responses with clear headings (##).\n"
                        "- ALWAYS use bullet points for explanations.\n"
                        "- NEVER write long paragraphs.\n"
                        "- Keep each bullet concise (1-2 sentences).\n"
                        "- Use numbered lists only for step-by-step troubleshooting.\n"
                        "- Highlight important warnings using **Warning**.\n"
                        "- Highlight recommendations using **Recommendation**.\n"
                        "- Use tables when comparing hardware.\n"
                        "- End every response with a '## Next Step' section whenever additional information is needed.\n\n"

                        "## Troubleshooting Guidelines\n"
                        "- Ask for missing system specifications before making assumptions.\n"
                        "- Request information such as CPU, GPU, RAM, motherboard, PSU, storage, operating system, monitor resolution, and game title when relevant.\n"
                        "- Explain the reason behind each recommendation.\n"
                        "- Prioritize practical and safe troubleshooting steps.\n\n"

                        "## Recommendation Guidelines\n"
                        "- Recommend reliable and compatible hardware.\n"
                        "- Consider budget, performance, upgrade path, power requirements, and thermal performance.\n"
                        "- Mention trade-offs when multiple options exist.\n"
                        "- Never recommend unnecessary upgrades.\n\n"

                        "## Formatting Requirements\n"
                        "- Every answer MUST contain at least one Markdown heading.\n"
                        "- Every explanation MUST be written as bullet points.\n"
                        "- Avoid paragraphs longer than two lines.\n"
                        "- Never return plain text without formatting.\n\n"

                        "## Example Format\n\n"

                        "## Diagnosis\n"
                        "- The GPU temperature is higher than expected during gaming.\n"
                        "- CPU utilization appears normal.\n"
                        "- The issue is likely related to airflow or cooling.\n\n"

                        "## Recommendations\n"
                        "- Update the graphics driver to the latest stable version.\n"
                        "- Clean dust from fans and heatsinks.\n"
                        "- Verify that all case fans are functioning correctly.\n"
                        "- Enable XMP/EXPO if supported by your RAM.\n\n"

                        "## Next Step\n"
                        "- Please provide your CPU, GPU, RAM, motherboard, PSU, monitor resolution, and the game you are playing."
                    )
                }
            ]

            # Add previous messages

            VALID_ROLES = {"user", "assistant", "system"}

            for message in history:

                if message["role"] not in VALID_ROLES:
                    continue

                messages.append(
                    {
                        "role": message["role"],
                        "content": message["content"]
                    }
                )

            # -------------------------
            # Execute Tool (if needed)
            # -------------------------

            tool_result = await self.process_tools(prompt)

            if tool_result and not isinstance(tool_result, dict):
                self.db_service.save_message(
                    session_id=session_id,
                    role="system",
                    content=tool_result.model_dump_json(indent=2)
                )

            if tool_result:

                # Missing parameters
                if isinstance(tool_result, dict):

                    missing = ", ".join(tool_result["fields"])

                    yield (
                        f"## Missing Information\n\n"
                        f"- Please provide: **{missing}**."
                    )

                    return

                # Tool executed successfully
                messages.append(
                    {
                        "role": "system",
                        "content": (
                            "The following data was returned from a trusted backend tool.\n\n"
                            "Treat these values as accurate.\n"
                            "Do not recalculate or modify them.\n\n"
                            f"{tool_result.model_dump_json(indent=2)}\n\n"
                            "Generate a helpful response for the user using Markdown."
                        )
                    }
                )

            # Current user message

            messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            # -------------------------
            # Groq streaming response
            # -------------------------

            stream = await self.client.chat.completions.create(

                model=self.model,

                messages=messages,

                stream=True
            )

            assistant_response = ""

            async for chunk in stream:

                if (
                    chunk.choices
                    and chunk.choices[0].delta.content
                ):

                    token = chunk.choices[0].delta.content

                    assistant_response += token

                    yield token

            # -------------------------
            # Save assistant response
            # -------------------------

            self.db_service.save_message(

                session_id=session_id,

                role="assistant",

                content=assistant_response

            )

        except Exception as e:

            yield f"\n[Groq API Backend Error: {str(e)}]"