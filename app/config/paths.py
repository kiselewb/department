from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_FILE = LOGS_DIR / "logs.log"
