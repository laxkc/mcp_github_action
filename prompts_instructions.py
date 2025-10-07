def github_logs_analysis_prompt(run_id: str, logs: str) -> str:
    """
    Professional prompt template to summarize GitHub Actions logs and suggest context-aware fixes if needed.
    """
    return f"""
You are a senior DevOps engineer analyzing GitHub Actions workflow logs.

Workflow Run ID: **{run_id}**

Logs:
{logs}

Task:
1. Provide a **structured summary** of the workflow:
   - Overall status (success, failure, warnings)
   - Key steps executed
   - Any failed steps or errors
   - Notable durations or bottlenecks
   - Final outcome

2. If there are errors or failures, provide a **technical analysis and recommended fixes**:
   - **Issue Summary:** Brief explanation of what failed
   - **Root Cause:** Likely reason for failure (e.g., syntax error, dependency issue, permission problem)
   - **Suggested Fix:** Clear, actionable steps to resolve the issue
   - **Prevention Tip:** Guidance to avoid similar failures in the future

Requirements:
- Format the summary in **concise bullet points**
- Provide **precise, technical guidance** for any errors
- Avoid generic or vague recommendations
    """.strip()
