import logging
import logging.config
import os
from pathlib import Path

LOGGING_CONFIG_PATH = Path(__file__).resolve().parent / 'src' / 'utils' / 'logging.conf'
REPO_DESTINATION_DIRECTORY = os.environ.get("CUSTOM_REPO_DESTINATION_DIRECTORY") != "none" and os.environ.get("CUSTOM_REPO_DESTINATION_DIRECTORY") or "repos"

logging.config.fileConfig(LOGGING_CONFIG_PATH, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from src.ingestion.scanner import scan_repo
from src.ingestion.loader import clone_or_update


if __name__ == "__main__":
    logger.info("Starting Lighthouse...")
    repo_url = "https://remira@dev.azure.com/remira/UnifiedCommercePlatform/_git/UCP_Frontend"
    local_path = REPO_DESTINATION_DIRECTORY+ "/UCP_Frontend"
    clone_or_update(repo_url, local_path)
    scan_repo(Path(local_path))