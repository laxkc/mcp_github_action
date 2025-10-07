# 🚀 MCP Github Action

## Trigger, monitor, and debug GitHub Actions from your IDE or chat — without leaving your flow.

>"MCP github Actions is an open-source MCP (Model Context Protocol) server that wraps the GitHub Actions API, enabling AI agents (or CLI tools) to run workflows, fetch logs, re-run jobs, and approve deployments — all via natural language or simple commands in Slack, VS Code, JetBrains, or terminal."

## Why MCP Actions?
GitHub Actions is powerful — but debugging CI failures means context-switching to the browser, scrolling through noisy logs, and clicking buttons.

**With MCP Actions, you can:**

`/gh run ci on feature/login-ui`

`→ ✅ Started workflow #42`

`→ 📋 12 tests passed | 0 failed`

`→ 🔗 View run: https://github.com/.../runs/42`

**Or in VS Code:**
>“Show me the latest CI failure for main”

**And get:**

>❌ Failed: build step exited with code 1 <br>
>📄 Log snippet: Error: Cannot find module 'react' <br>
>💡 Suggestion: Did you forget to run npm install? <br>
>🔄 [Re-run] | [Open in GitHub] | [Debug locally] 

**No more tab-switching. No more log archaeology.**


## Features

| **Capability**              | **Command Example**                                                   | **Supported Clients**     |
|-----------------------------|----------------------------------------------------------------------|---------------------------|
| **Run workflow**            | `run_workflow(branch="main")`                                        | Slack, VS Code, CLI       |
| **Get summarized logs**     | `get_logs(run_id=latest, format="summary")`                          | All                       |
| **Re-run failed workflow**  | `rerun_workflow(run_id=42)`                                          | All                       |
| **Approve deployment**      | `approve_environment(env="prod", run_id=42)`                         | Slack, Teams              |
| **Validate workflow YAML**  | `validate_workflow(path=".github/workflows/ci.yml")`                 | CLI, IDE                  |
| **Local simulation (WIP)**  | `simulate_run(branch="test")`                                        | CLI                       |

## How It Works
<img width="3840" height="267" alt="Untitled diagram _ Mermaid Chart-2025-10-06-144729" src="https://github.com/user-attachments/assets/65ffaf1a-a85f-45c6-9783-6e66d3f2a3ed" />

The **MCP server**:

- Authenticates with **GitHub**
- Triggers workflows via  
  `POST /repos/{owner}/{repo}/actions/workflows/{id}/dispatches`
- Polls for completion  
- Fetches logs, parses them, and returns **structured, actionable insights**

---

## Use Cases

### 🔍 Debug Faster
**“Why did CI fail on main last night?”**  
→ Get error summary + suggested fix directly in chat.

---

### 🚦 Approve Deployments from Slack
**“Approve prod deploy #89”**  
→ Bypass GitHub UI while keeping the **audit trail preserved**.

---

### 🧪 Test Workflows Before Merging
**“Validate this workflow file”**  
→ Catch **YAML errors** before they break CI.


# mcp_github_action
