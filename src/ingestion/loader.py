import logging
import os
import git

logger = logging.getLogger(__name__)

def clone_or_update(repo_url: str, local_path: str):
    if (os.path.exists(local_path) and os.path.isdir(local_path) and os.path.exists(os.path.join(local_path, '.git'))):
        logger.info(f"Updating existing repository at {local_path}...")
        repo = git.Repo(local_path)
        origin = repo.remotes.origin
        origin.pull()
    else:
        logger.info(f"Cloning new repository from {repo_url} to {local_path}...")
        git.Repo.clone_from(repo_url, local_path)