import os
import subprocess
from pathlib import Path

def load_openai_api_key(env_file_path: Path = None) -> str:
    """Loads OpenAI API key from environment, 1Password CLI, or fallback .env file."""
    # 1. Check if already in environment
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key

    # 2. Try loading from 1Password CLI
    try:
        key = subprocess.check_output(
            ["op", "read", "op://Personal/OpenAIDataTalk/credential"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        os.environ["OPENAI_API_KEY"] = key
        return key
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # 3. Fallback: read from .env file
    # By default, look for the .env file in the same directory as this utils.py (the project root)
    if env_file_path is None:
        env_file_path = Path(__file__).parent / ".env"

    if env_file_path.exists():
        for line in env_file_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("OPENAI_API_KEY=") and not line.startswith("#"):
                key = line.split("=", 1)[1].strip()
                os.environ["OPENAI_API_KEY"] = key
                return key

    raise EnvironmentError(
        f"OPENAI_API_KEY not found in environment, 1Password, or {env_file_path.resolve()}. "
        "Please ensure you are signed in to 1Password or have created the fallback file."
    )
