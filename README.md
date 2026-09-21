# UnifiedGov AI – Agentic Fraud Detection Platform

UnifiedGov AI is a cross-department AI system designed to identify inconsistencies and potential fraud by analyzing information across multiple government departments.

The project brings together department-specific agents, an orchestration layer, fraud risk scoring, and explainability to produce a final risk assessment for a citizen record.

---

## Problem

Government information is often distributed across different departments and systems.

When information from departments such as Housing, Electricity, and Tax does not match, manually identifying these inconsistencies can be difficult and time-consuming.

UnifiedGov AI explores how an agent-based AI system can coordinate information from different departments and assist in identifying suspicious records.

---

## What the System Does

For a selected citizen record, the system:

1. Collects information from department-specific datasets.
2. Runs verification through specialized AI agents.
3. Coordinates the agents using an orchestration layer.
4. Identifies inconsistencies across the collected information.
5. Calculates a fraud risk score.
6. Generates an explanation for the resulting risk level.
7. Produces a final decision report with a recommendation.

---

## Architecture

```text
                    Citizen Record
                          |
                          v
                +----------------------+
                |  Agent Orchestrator  |
                +----------+-----------+
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
   Housing Agent    Electricity Agent    Tax Agent
          |                |                |
          +----------------+----------------+
                           |
                           v
                    Snitch Agent
                           |
                           v
                  Fraud Risk Scoring
                           |
                           v
                  Explainability Agent
                           |
                           v
                  Final Decision Report
