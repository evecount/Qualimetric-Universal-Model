---
description: Check local environment for tools (Python, GraphQL, Node.js) and prepare workspace for Sovereign Integrity hooks.
---

# Workflow: Environment Architect (The Portability Agent)

This workflow ensures the host environment is mission-ready for deploying and testing Sovereign Integrity hooks.

## Steps

1. **Environment Audit**:
   // turbo
   - Check for `python --version` (Required: 3.8+).
   - Check for `node --version` (Required for future Stage 5 integrations).
   - Verify `pip` packages: `fastapi`, `uvicorn`, `requests`, `jinja2`.

2. **Dependency Harmonization**:
   // turbo-all
   - If Python packages are missing, run `pip install -r requirements.txt` (or install individual packages).
   - Prepare a `.env` template if one does not exist.

3. **Workspace Readiness**:
   - Ensure `sovereign-gateway/static` and `sovereign-gateway/templates` are correctly populated.
   - Run `python sovereign-gateway/verify_gateway.py` to confirm local baseline.

4. **Sovereignty Hook Injection**:
   - Prepare a "Mock GraphQL" endpoint if testing specific Stage 4 integration hooks.
