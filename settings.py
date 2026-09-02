import os
from dataclasses import dataclass
from pathlib import Path
from typing import FrozenSet

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Required environment variable {name} is not set")
    return value


def _allowed_user_ids() -> FrozenSet[int]:
    raw_ids = _required("ALLOWED_USER_IDS")
    try:
        user_ids = frozenset(int(value.strip()) for value in raw_ids.split(",") if value.strip())
    except ValueError as exc:
        raise RuntimeError("ALLOWED_USER_IDS must contain comma-separated Telegram user IDs") from exc
    if not user_ids:
        raise RuntimeError("ALLOWED_USER_IDS must contain at least one Telegram user ID")
    return user_ids


def _path(name: str, default: str = "") -> Path:
    value = os.getenv(name, default).strip()
    if not value:
        raise RuntimeError(f"Required environment variable {name} is not set")
    path = Path(value).expanduser()
    return path if path.is_absolute() else BASE_DIR / path


@dataclass(frozen=True)
class Settings:
    bot_token: str
    allowed_user_ids: FrozenSet[int]
    google_credentials_file: Path
    google_spreadsheet_id: str
    google_sheet_id: int
    database_path: Path


def load_settings() -> Settings:
    load_dotenv(BASE_DIR / ".env")
    credentials_file = _path("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_file.is_file():
        raise RuntimeError(f"Google credentials file does not exist: {credentials_file}")
    try:
        sheet_id = int(_required("GOOGLE_SHEET_ID"))
    except ValueError as exc:
        raise RuntimeError("GOOGLE_SHEET_ID must be an integer") from exc
    return Settings(
        bot_token=_required("BOT_TOKEN"),
        allowed_user_ids=_allowed_user_ids(),
        google_credentials_file=credentials_file,
        google_spreadsheet_id=_required("GOOGLE_SPREADSHEET_ID"),
        google_sheet_id=sheet_id,
        database_path=_path("DATABASE_PATH", "db/Metals_with_data.db"),
    )


settings = load_settings()
