# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Smarter Scheduling

Our updated backend includes numerous quality-of-life and algorithmic refactors to improve schedule usability:
- **String Filtering**: Safely retrieve tasks by Completion Status (Completed/Pending) or precisely by Pet Name directly from an `Owner`'s dataset.
- **Smart Sorting**: Uses inline lambda properties to accurately parse time strings chronologically rather than sequentially placing random assignments on the schedule.
- **Lightweight Conflict Check**: Checks time parameters for overlapping entries across both a single pet and an owner's entire household, outputting accessible, non-crashing `.warning` messages instead of failing the compiler.
- **Recurring Engine**: Re-queues tasks flagged as `"daily"` or `"weekly"` by deeply cloning the finished element, creating a new `"pending"` task, and advancing Python's `timedelta()` parameter by either 1 day or 7 days natively.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
