import logging
import time
from .config import COST_PER_1K_TOKENS

logger = logging.getLogger("openai_service")

def log_openai_call(model, prompt_tokens, completion_tokens, duration, status="SUCCESS"):
    """Logue les détails d'un appel API avec estimation des coûts."""
    total_tokens = prompt_tokens + completion_tokens
    
    # Estimation simple du coût
    cost = (prompt_tokens / 1000 * COST_PER_1K_TOKENS["input"]) + \
           (completion_tokens / 1000 * COST_PER_1K_TOKENS["output"])
    
    log_msg = (
        f"[OpenAI Call] Status: {status} | Model: {model} | "
        f"Tokens: {total_tokens} (P:{prompt_tokens}, C:{completion_tokens}) | "
        f"Durée: {duration:.2f}s | Coût Est.: ${cost:.5f}"
    )
    
    if status == "SUCCESS":
        logger.info(log_msg)
    else:
        logger.error(log_msg)
