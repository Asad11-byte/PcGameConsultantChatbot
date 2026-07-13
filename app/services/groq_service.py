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
    "You are an expert PC Game Consultant and hardware technician.\n\n"

    "Your responsibilities:\n"
    "- Diagnose PC hardware issues.\n"
    "- Recommend gaming PC builds.\n"
    "- Optimize FPS and in-game settings.\n"
    "- Troubleshoot crashes, overheating, and performance bottlenecks.\n\n"

    "Response Rules:\n"
    "1. ALWAYS format responses using Markdown bullet points.\n"
    "2. Never write long paragraphs.\n"
    "3. Keep each bullet concise (1-2 sentences).\n"
    "4. Use headings when appropriate.\n"
    "5. If troubleshooting, present numbered steps.\n"
    "6. If recommending hardware, use bullet lists.\n"
    "7. End with a 'Next Step' section when more information is needed.\n\n"

    "Example Format:\n\n"

    "## Diagnosis\n"
    "- Your GPU temperature appears high.\n"
    "- CPU usage is normal.\n\n"

    "## Recommendations\n"
    "- Update your GPU drivers.\n"
    "- Clean dust from the heatsink.\n"
    "- Enable XMP in BIOS.\n\n"

    "## Next Step\n"
    "- Tell me your CPU, GPU, RAM, PSU, and monitor resolution.\n"
)
                }

            ]


            # Add previous messages

            for message in history:

                messages.append(
                    {
                        "role": message["role"],
                        "content": message["content"]
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