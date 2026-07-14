import re
import unicodedata
from dataclasses import dataclass


@dataclass
class SecurityResult:
    allowed: bool
    message: str
    cleaned_prompt: str


class PromptSecurityService:

    MAX_PROMPT_LENGTH = 4000

    # Prompt Injection / Jailbreak Patterns
    BLOCK_PATTERNS = [

        r"ignore\s+(all\s+)?previous\s+instructions",

        r"forget\s+(all\s+)?instructions",

        r"system\s+prompt",

        r"developer\s+message",

        r"hidden\s+instructions",

        r"reveal\s+your\s+instructions",

        r"print\s+your\s+prompt",

        r"show\s+your\s+prompt",

        r"internal\s+prompt",

        r"jailbreak",

        r"do\s+anything\s+now",

        r"\bdan\b",

        r"simulate\s+chatgpt",

        r"act\s+as\s+developer",

        r"disable\s+safety",

        r"bypass\s+security",

        r"override\s+instructions",

        r"ignore\s+system",

        r"execute\s+code",

        r"run\s+shell",

        r"os\.system",

        r"subprocess",

        r"eval\s*\(",

        r"exec\s*\(",

        r"api[_\s]?key",

        r"access\s+token",

        r"secret",

        r"password",

        r"environment\s+variables",

        r"\.env"

    ]

    # Allowed chatbot topics

    ALLOWED_TOPICS = [

        "gaming",

        "pc",

        "gpu",

        "cpu",

        "motherboard",

        "ram",

        "ssd",

        "psu",

        "windows",

        "fps",

        "valorant",

        "cs2",

        "fortnite",

        "minecraft",

        "amd",

        "intel",

        "nvidia",

        "rtx",

        "rx",

        "monitor",

        "bios",

        "driver",

        "overclock",

        "temperature"

    ]

    def normalize(self, text: str):

        text = unicodedata.normalize("NFKC", text)

        text = text.replace("\x00", "")

        return text.strip()

    def detect_prompt_injection(self, prompt):

        lower = prompt.lower()

        for pattern in self.BLOCK_PATTERNS:

            if re.search(pattern, lower):

                return True

        return False

    def validate_length(self, prompt):

        return len(prompt) <= self.MAX_PROMPT_LENGTH

    def validate_topic(self, prompt):

        prompt = prompt.lower()

        return any(topic in prompt for topic in self.ALLOWED_TOPICS)

    def validate(self, prompt: str):

        cleaned = self.normalize(prompt)

        if not self.validate_length(cleaned):

            return SecurityResult(
                False,
                "Prompt is too long.",
                cleaned
            )

        if self.detect_prompt_injection(cleaned):

            return SecurityResult(
                False,
                "Prompt rejected for security reasons.",
                cleaned
            )

        # Optional:
        # Uncomment if you ONLY want gaming-related questions.
        #
        # if not self.validate_topic(cleaned):
        #
        #     return SecurityResult(
        #         False,
        #         "Please ask gaming or PC related questions.",
        #         cleaned
        #     )

        return SecurityResult(
            True,
            "OK",
            cleaned
        )