import os
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

class GroqService:
    def __init__(self):
        self.client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        # Using a highly capable model for reasoning through complex hardware configurations
        self.model = "llama-3.3-70b-versatile" 

    async def get_chat_stream(self, prompt: str):
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are an expert PC Game Consultant and hardware technician. Your goal is to help "
                            "users diagnose hardware issues, recommend building specs, optimize in-game settings, "
                            "and troubleshoot system performance bottlenecks (like overheating, crashes, or low FPS).\n\n"
                            "Guidelines:\n"
                            "- Provide clear, technical, yet highly actionable advice.\n"
                            "- When users have performance issues, ask about or consider their specs (CPU, GPU, RAM) "
                            "and environmental factors (thermals, background apps).\n"
                            "- If troubleshooting hardware failures (e.g., power failures, component short circuits), "
                            "guide them systematically through logical isolation steps (checking components, power lines, or physical signs)."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"\n[Groq API Backend Error: {str(e)}]"