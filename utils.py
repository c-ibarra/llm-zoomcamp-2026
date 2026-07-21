import os
import subprocess

# NOTE: secrets are always resolved from the process environment or the 1Password
# CLI, never from a config file on disk (.env, .env.tpl, etc). A file can be left
# behind, copied, or accidentally committed; 1Password can't be.


def _read_from_1password(op_path: str) -> str:
    """Reads a single secret value from the 1Password CLI (`op read`)."""
    try:
        return subprocess.check_output(
            ["op", "read", op_path],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise EnvironmentError(
            f"Could not resolve secret from 1Password at {op_path}. "
            "Make sure the 1Password CLI ('op') is installed and you are signed in."
        ) from e


def load_openai_api_key() -> str:
    """Loads OPENAI_API_KEY from environment or 1Password CLI."""
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key
    key = _read_from_1password("op://Personal/OpenAIDataTalk/credential")
    os.environ["OPENAI_API_KEY"] = key
    return key


def load_logfire_token() -> str:
    """Loads LOGFIRE_TOKEN (write token) from environment or 1Password CLI."""
    token = os.environ.get("LOGFIRE_TOKEN")
    if token:
        return token
    token = _read_from_1password("op://Personal/Pydantic/Token")
    os.environ["LOGFIRE_TOKEN"] = token
    return token


def load_logfire_read_token() -> str:
    """Loads LOGFIRE_READ_TOKEN from environment or 1Password CLI."""
    token = os.environ.get("LOGFIRE_READ_TOKEN")
    if token:
        return token
    token = _read_from_1password("op://Personal/Pydantic/TokenRead")
    os.environ["LOGFIRE_READ_TOKEN"] = token
    return token
