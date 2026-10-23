import os
from datetime import datetime

# ANSI Color & Style Sequences
RESET = "\033[0m"
BOLD = "\033[1m"
GRAY = "\033[90m"

# Level Configurations: (ANSI Color, Icon, Tag Label)
LEVEL_MAP = {
    "INFO":    ("\033[36m", "ℹ", "INFO"),       # Cyan
    "STEP":    ("\033[34m", "➤", "STEP"),       # Blue
    "TOOL":    ("\033[35m", "⚙", "TOOL"),       # Magenta
    "RESULT":  ("\033[32m", "✔", "RESULT"),     # Green
    "SUCCESS": ("\033[32m", "✔", "SUCCESS"),    # Green
    "WARN":    ("\033[33m", "⚠", "WARN"),       # Yellow
    "WARNING": ("\033[33m", "⚠", "WARN"),       # Yellow
    "ERROR":   ("\033[31m", "✖", "ERROR"),      # Red
    "DEBUG":   ("\033[90m", "🔍", "DEBUG"),     # Gray
}


def _detect_level(message: str, current_level: str) -> str:
    """Auto-detect level if left as default INFO."""
    if current_level != "INFO":
        return current_level

    msg_lower = message.lower()
    if msg_lower.startswith("step ") or " step " in msg_lower:
        return "STEP"
    if "called with args" in msg_lower or "calling tool" in msg_lower:
        return "TOOL"
    if "tool result" in msg_lower or "result:" in msg_lower:
        return "RESULT"
    if "failed" in msg_lower or "error" in msg_lower or "exception" in msg_lower:
        return "ERROR"
    if "warn" in msg_lower:
        return "WARN"

    return "INFO"


def log(message, level="INFO"):
    """Print stylish, colored, and structured logs to the console."""
    # Check if debug logging is enabled (defaults to True)
    if os.getenv("DEBUG", "true").lower() not in ("true", "1", "yes"):
        return

    timestamp = datetime.now().strftime("%H:%M:%S")
    msg_str = str(message)

    resolved_level = _detect_level(msg_str, str(level).strip().upper())
    no_color = bool(os.getenv("NO_COLOR"))

    color, icon, tag = LEVEL_MAP.get(
        resolved_level,
        ("\033[37m", "•", resolved_level[:6])
    )

    if no_color:
        badge = f"[{tag:<6}]"
        print(f"[{timestamp}] {badge} {msg_str}", flush=True)
    else:
        badge = f"{color}{BOLD}[{icon} {tag:<6}]{RESET}"
        print(f"{GRAY}[{timestamp}]{RESET} {badge} {msg_str}", flush=True)
