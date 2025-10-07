from mcp.server.fastmcp import FastMCP
from github_client import GitHubClient
from prompts_instructions import github_logs_analysis_prompt
from git_context import detect_git_context
import asyncio

# Create an instance of FastMCP
mcp = FastMCP("github_actions_mcp")

# Create an instance of GitHubClient
github_client = GitHubClient()


# GitHub session class
class GitHubSession:
    """Dynamic GitHub session for any repo/branch"""

    def __init__(self, owner: str, repo: str, branch: str):
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.workflow_id = None
        self.run_id = None
        self.latest_run = None
        self.logs = None

    async def get_workflow_id(self):
        if self.workflow_id is None:
            self.workflow_id = await github_client.get_workflow_id(
                self.owner, self.repo, workflow_name=None
            )
        return self.workflow_id

    async def get_latest_run_id(self):
        if self.run_id is None:
            self.run_id, self.latest_run = await github_client.get_latest_run_id(
                self.owner, self.repo, self.branch, self.workflow_id
            )
        return self.run_id

    async def get_logs(self):
        if self.logs is None:
            self.logs = await github_client.get_logs(
                self.owner, self.repo, self.run_id
            )
        return self.logs


async def get_dynamic_session():
    """Detect Git context dynamically and create a session"""
    git_context = detect_git_context()
    if not git_context["owner"] or not git_context["repo"] or not git_context["branch"]:
        raise RuntimeError("Git context not detected. Are you in a GitHub repo?")
    session = GitHubSession(
        git_context["owner"], git_context["repo"], git_context["branch"]
    )
    await session.get_workflow_id()
    await session.get_latest_run_id()
    await session.get_logs()
    return session



""" MCP Tools """

@mcp.tool("trigger_workflow")
async def trigger_workflow():
    """Trigger a workflow dynamically based on current repo"""
    try:
        session = await get_dynamic_session()
        return await github_client.trigger_workflow(
            session.owner, session.repo, session.workflow_id, session.branch
        )
    except Exception as e:
        return f"Error triggering workflow: {e}"


@mcp.tool("get_logs")
async def get_logs():
    """Get logs for the latest run dynamically"""
    try:
        session = await get_dynamic_session()
        return await session.get_logs()
    except Exception as e:
        return f"Error getting logs: {e}"


@mcp.tool("rerun_workflow")
async def rerun_workflow():
    """Re-run the latest workflow dynamically"""
    try:
        session = await get_dynamic_session()
        return await github_client.rerun_workflow(
            session.owner, session.repo, session.run_id
        )
    except Exception as e:
        return f"Error re-running workflow: {e}"


""" MCP Prompts """

@mcp.prompt("summarize_logs")
def summarize_logs():
    """Summarize latest GitHub Actions logs for current repo"""
    try:
        session = asyncio.run(get_dynamic_session())
        if not session.logs:
            return "No logs found for the latest run."
        return github_logs_analysis_prompt(session.run_id, session.logs)
    except Exception as e:
        return f"Error summarizing logs: {e}"


""" Main Server """

def main():
    print("GitHub MCP Server is running...")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
