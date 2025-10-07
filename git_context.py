import subprocess
import re
import sys

def detect_git_context():
    """
    Detects GitHub repo owner, repo name, and current branch from local git config.
    Returns dict like {'owner': '...', 'repo': '...', 'branch': '...'}
    """
    try:
        # Get remote origin URL
        remote_url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        # Example: git@github.com:laxmankc/mcp_server_cicd.git
        # or https://github.com/laxmankc/mcp_server_cicd.git
        match = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)", remote_url)
        if not match:
            raise ValueError("Not a GitHub repo")

        owner, repo = match.group("owner"), match.group("repo")

        # Get current branch
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        return {"owner": owner, "repo": repo, "branch": branch}

    except Exception as e:
        print(f"Git context detection failed: {e}", file=sys.stderr)
        return {"owner": None, "repo": None, "branch": None}
