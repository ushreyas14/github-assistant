import git
from pathlib import Path

def clone_or_pull(repo_url: str, base_dir: str = "./repos") -> tuple:
    # Extract repo name from URL
    # e.g. "https://github.com/pallets/flask" → "flask"
    repo_name  = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    local_path = str(Path(base_dir) / repo_name)
    path       = Path(local_path)

    if path.exists() and (path / ".git").exists():
        print(f"Repo exists. Pulling latest...")
        repo = git.Repo(local_path)
        repo.remotes.origin.pull()
    else:
        print(f"Cloning {repo_url}...")
        git.Repo.clone_from(repo_url, local_path)

    print(f"Repo ready at: {local_path}")
    return local_path, repo_name