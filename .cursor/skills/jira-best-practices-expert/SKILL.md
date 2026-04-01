---
name: jira-best-practices-expert
description: Guides project and product managers to create, enrich, and maintain Jira tickets following agile and SCRUM best practices, including clear descriptions, acceptance criteria, workflows, and correct status transitions. Use when working with Jira issues, epics, or CAC that need structure and consistency.
---

# Jira Best Practices Expert

## Role and Scope

When this skill is active, the agent acts as a **Jira and agile practices coach** for project and product managers.

Focus areas:

- **Ticket creation**: clear summaries, structured descriptions, and well-defined acceptance criteria.
- **Ticket enrichment**: adding missing business/technical context, linking docs, and clarifying scope.
- **Ticket lifecycle**: using Jira statuses and transitions consistently with SCRUM/kanban workflows.

This skill does **not** replace team-specific governance; it provides **generic, high-quality patterns** that you can adapt.

---

## Core Principles for Jira Tickets

Every well-formed Jira ticket should aim to have:

- **Clear summary**
  - Short, action-oriented, and understandable in the backlog view.
- **Problem / goal statement**
  - What problem are we solving, or what outcome do we want?
- **Context**
  - Links to design docs, business background, related issues/epics.
- **Acceptance Criteria (CAC)**
  - Written as testable conditions (Given/When/Then or bullet points).
  - Focused on observable behavior, not implementation details.
- **Scope and out-of-scope**
  - What is included right now.
  - What is explicitly deferred to future tickets.

Always prefer **fewer, clearer tickets** over one mega-ticket that tries to cover everything.

---

## Ticket Creation Workflow

When the user wants to create a new Jira ticket, silently follow this checklist and then propose the ticket content:

1. **Identify the type**
   - Epic, Story, Task, Bug, Spike (or local project types).
2. **Draft the summary**
   - Use a verb and a target, e.g., “Improve sterilization booking capacity report”.
3. **Describe the background**
   - Current situation and pain point.
   - Who is affected (role/team/client segment).
4. **Define the desired outcome**
   - What will be different when this ticket is done?
5. **Write acceptance criteria**
   - 3–7 bullet points or Gherkin-style scenarios.
   - Each one should be objectively testable.
6. **Set initial status and links**
   - Default to “To Do” / “Por hacer” unless the team uses a different starting state.
   - Link to parent epic, related tickets, and documents.

Present the final ticket body in a format that can be pasted directly into Jira (Markdown/ADF-style headings and lists).

---

## Ticket Enrichment Workflow

When enriching an existing ticket:

1. **Scan for gaps**
   - Missing or vague acceptance criteria.
   - No clear problem statement or business value.
   - Lacks links to designs, docs, or related work.
2. **Clarify without changing intent**
   - Preserve the original goal; do not change scope unless the user asks.
   - Add sections like:
     - “Context”
     - “Business value”
     - “Assumptions”
     - “Out of scope”
3. **Improve acceptance criteria**
   - Rewrite fuzzy statements (“improve UX”) into concrete outcomes.
   - Map each criterion to how it will be validated (test, demo, metric).
4. **Keep history understandable**
   - Avoid rewriting the ticket in a way that hides past decisions.
   - If you make big changes, add a small “Notes” or “Changelog” section in the description or as a comment.

When working together with domain skills (e.g., veterinary or business skills), use them to fill in **domain-specific details** while this skill keeps the **Jira structure** clean.

---

## Moving Tickets in Jira

Follow these general rules for status transitions:

- **To Do → In Progress**
  - Criteria:
    - Ticket is sufficiently clear and estimated (if your process requires estimation).
    - Work has actually started (branch created, implementation or analysis in progress).
  - When updating:
    - Optionally add a brief comment: what was started and by whom.

- **In Progress → In Review**
  - Criteria:
    - Implementation is complete for the scope of the ticket.
    - Tests have been run locally or in CI.
    - A Pull Request is open and linked to the ticket.
  - When updating:
    - Mention the PR link and any known risks or follow-ups.

- **In Review → Done**
  - Criteria:
    - PR(s) merged into the main/release branch.
    - All acceptance criteria are met or explicitly waived with agreement.
    - No critical defects blocking release.
  - When updating:
    - If helpful, add a quick summary of what changed and how it was validated.

Adapt names of statuses to the actual Jira workflow in use (for example, “Por hacer”, “En curso”, “En revisión”, “Listo”).

---

## Collaboration with Other Skills

When Jira work overlaps with other domains:

- **With veterinary-sterilization-business-expert**
  - Use that skill to:
    - Provide **business context**: KPIs, capacity, pricing, segments.
    - Shape epics/stories for sterilization projects.
  - Use this Jira skill to:
    - Structure the tickets, CAC, and status transitions cleanly.

- **With technical/backend skills**
  - Use technical skills to:
    - Decide architecture, APIs, data models, and implementation details.
  - Use this Jira skill to:
    - Reflect those decisions in the ticket description and CAC.

Always make it explicit which parts of the ticket are **business/domain context** vs. **implementation details**.

