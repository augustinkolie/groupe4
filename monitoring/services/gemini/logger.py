import logging
from .config import COST_PER_1M_TOKENS

logger = logging.getLogger("gemini_service")

def log_gemini_call(model, input_tokens, output_tokens, duration, status="SUCCESS", safety_ratings=None):
    """Logue les détails d'un appel API avec estimation des coûts et sécurité."""
    total_tokens = input_tokens + output_tokens
    
    # Estimation simple du coût (par million de tokens)
    cost = (input_tokens / 1_000_000 * COST_PER_1M_TOKENS["input"]) + \
           (output_tokens / 1_000_000 * COST_PER_1M_TOKENS["output"])
    
    safety_info = f" | Safety: {safety_ratings}" if safety_ratings else ""
    
    log_msg = (
        f"[Gemini Call] Status: {status} | Model: {model} | "
        f"Tokens: {total_tokens} (I:{input_tokens}, O:{output_tokens}) | "
        f"Durée: {duration:.2f}s | Coût Est.: ${cost:.6f}{safety_info}"
    )
    
    if status == "SUCCESS":
        logger.info(log_msg)
    else:
        logger.error(log_msg)
