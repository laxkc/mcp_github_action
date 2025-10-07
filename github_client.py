import os
from dotenv import load_dotenv
import httpx


# Load the env variables
load_dotenv()

# GitHub token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Headers for the GitHub API
Headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

# Base URL for the GitHub API
BaseURL = "https://api.github.com"

""" 
GitHub client class to interact with the GitHub API
"""
class GitHubClient:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.headers = Headers
        self.base_url = BaseURL
    
    """ 
    Get the workflow ID based on name or path.
    """ 
    async def get_workflow_id(self, owner, repo, workflow_name=None, workflow_path=None):
        """
        Returns the workflow ID based on name or path.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/actions/workflows"
        try:
            response = await self.client.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            workflows = data.get("workflows", [])
            if not workflows:
                raise ValueError(f"No workflows found in {owner}/{repo}")

            if workflow_path:
                for wf in workflows:
                    if wf["path"] == workflow_path:
                        return wf["id"]
            if workflow_name:
                for wf in workflows:
                    if wf["name"] == workflow_name:
                        return wf["id"]
            return workflows[0]["id"]
        except Exception as e:
            print(f"Error getting workflow ID: {e}")
            return None

    
    """ 
    Get the latest run ID for a given branch or workflow.
    """ 
    async def get_latest_run_id(self, owner, repo, branch=None, workflow_id=None):
        """
        Fetch the latest workflow run_id for a given branch or workflow.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/actions/runs"
        params = {} 
        if branch:
            params["branch"] = branch
        if workflow_id:
            params["workflow_id"] = workflow_id

        try:
            response = await self.client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            runs = data.get("workflow_runs", [])
            if not runs:
                raise ValueError(f"No runs found for {repo} on branch {branch or 'any'}")

            latest_run = runs[0]
            return latest_run["id"], latest_run
        except Exception as e:
            print(f"Error getting latest run ID: {e}")
            return None, None
        
    """ 
    Trigger a workflow
    """
    async def trigger_workflow(self, owner: str, repo: str, workflow_id: str, branch: str):
        try: 
            response = await self.client.post(f"{self.base_url}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches", headers=self.headers, json={"ref": branch})
            return response.json()
        except Exception as e:
            print(f"Error triggering workflow: {e}")
            return None
    
    """ 
    Get logs for a workflow
    """
    async def get_logs(self, owner: str, repo: str, run_id: str):
        try:
            response = await self.client.get(f"{self.base_url}/repos/{owner}/{repo}/actions/runs/{run_id}/logs", headers=self.headers)
            return response.json()
        except Exception as e:
            print(f"Error getting logs: {e}")
            return None
    
    """ 
    Re-run a workflow
    """
    async def rerun_workflow(self, owner: str, repo: str, run_id: str):
        try:
            response = await self.client.post(f"{self.base_url}/repos/{owner}/{repo}/actions/runs/{run_id}/rerun", headers=self.headers)
            return response.json()
        except Exception as e:
            print(f"Error re-running workflow: {e}")
            return None

