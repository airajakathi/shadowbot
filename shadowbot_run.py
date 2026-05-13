"""
ShadowBot — Main Runner
Telegram bot with auto model routing using StepFun API.

Models:
  step-3.5-flash  → fast/simple tasks (chat, Q&A, summaries)
  step-3.6        → complex tasks (reasoning, code, analysis)
  step-image-edit-2 → image generation/editing tasks

Run:
    python shadowbot_run.py
"""

import os
import asyncio
import logging
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
log = logging.getLogger("shadowbot")

# ── StepFun model profiles ───────────────────────────────────────────────────
STEPFUN_BASE_URL = os.environ["OPENAI_API_BASE"]
STEPFUN_API_KEY  = os.environ["OPENAI_API_KEY"]

MODEL_FAST  = os.getenv("SHADOWBOT_MODEL_FAST",  "step-3.5-flash")
MODEL_MAIN  = os.getenv("SHADOWBOT_MODEL_MAIN",  "step-3.6")
MODEL_IMAGE = os.getenv("SHADOWBOT_MODEL_IMAGE", "step-image-edit-2")

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]


def select_model(message: str) -> str:
    """
    Auto-select the best StepFun model based on message content.
      - Image-related keywords → step-image-edit-2
      - Complex/code/analysis  → step-3.6
      - Everything else        → step-3.5-flash
    """
    text = message.lower()
    image_keywords = [
        "image", "picture", "photo", "draw", "generate image",
        "edit image", "create image", "visualize", "illustration"
    ]
    complex_keywords = [
        "code", "debug", "algorithm", "analyze", "research", "explain",
        "compare", "evaluate", "plan", "strategy", "architecture",
        "write a", "build", "implement", "design", "reason", "calculate",
        "step by step", "detailed", "comprehensive"
    ]
    if any(kw in text for kw in image_keywords):
        return MODEL_IMAGE
    if any(kw in text for kw in complex_keywords) or len(text) > 200:
        return MODEL_MAIN
    return MODEL_FAST


def build_agent(model: str):
    """Build a ShadowBot agent for the given model."""
    from shadowbotagents import Agent
    return Agent(
        name="ShadowBot",
        role="Intelligent AI assistant",
        goal="Help users with any task efficiently and accurately",
        backstory=(
            "You are ShadowBot, a powerful AI assistant. "
            "You are precise, helpful, and adapt to the complexity of each task."
        ),
        llm=model,
        llm_config={
            "api_key": STEPFUN_API_KEY,
            "base_url": STEPFUN_BASE_URL,
        },
        verbose=False,
        markdown=True,
    )


async def run_telegram_bot():
    """Start the ShadowBot Telegram interface."""
    from shadowbot.bots.telegram import TelegramBot
    from shadowbotagents import Agent

    log.info("Starting ShadowBot Telegram bot...")
    log.info(f"  Fast model  : {MODEL_FAST}")
    log.info(f"  Main model  : {MODEL_MAIN}")
    log.info(f"  Image model : {MODEL_IMAGE}")
    log.info(f"  API base    : {STEPFUN_BASE_URL}")

    # Build a default agent with the main model
    agent = build_agent(MODEL_MAIN)

    class AutoRoutingTelegramBot(TelegramBot):
        """Extends TelegramBot to auto-select models per message."""

        async def process_message(self, message):
            selected = select_model(message.content or "")
            if selected != MODEL_MAIN:
                log.info(f"Auto-routing to model: {selected} for message length {len(message.content or '')}")
                self.agent = build_agent(selected)
            else:
                self.agent = agent
            return await super().process_message(message)

    bot = AutoRoutingTelegramBot(
        token=TELEGRAM_TOKEN,
        agent=agent,
    )

    await bot.start()


if __name__ == "__main__":
    asyncio.run(run_telegram_bot())
