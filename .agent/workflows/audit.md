---
description: Perform a 'Structural Signature' audit on existing auth logic and identify deterministic vulnerabilities.
---

# Workflow: Automated Auditor (The Revenue Multiplier Agent)

This workflow acts as a proactive security layer, identifying deterministic "Governance Gaps" and proposing Sovereign replacements.

## Steps

1. **Strategic Discovery**:
   - Search the codebase for deterministic auth patterns: `JWT`, `API_KEY`, `OAuth`, `Static Secrets`.
   - Use `grep_search` to find "deterministic" or "centralized" trust assumptions.

2. **Vulnerability Assessment**:
   - Analyze how an AI Agent could "hallucinate" an authorized call to these endpoints without a hardware-rooted anchor.
   - Categorize risks into: **Total Asset Loss**, **Identity Spoofing**, and **Deepfake Intent**.

3. **USP Injection Proposal**:
   - Generate a refactoring plan to wrap existing authentication logic in a **Sovereign Passport** verification gate.
   - Show a "Before vs After" comparison of the security posture.

4. **Audit Report**:
   - Generate an `AUDIT_REPORT.md` that quantifies the "Cost of Failure" versus the "Cost of Trust" for the analyzed service.
