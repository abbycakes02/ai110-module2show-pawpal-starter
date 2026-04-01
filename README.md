# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Core Features & Algorithms

PawPal+ is driven by a smart, algorithmic backend designed to make pet care intuitive and conflict-free. Here are the core features implemented into the system:

- **Chronological Sorting by Time**: Implements a robust sorting algorithm leveraging inline lambda functions to accurately parse and chronologically order 24-hour "HH:MM" time strings, ensuring tasks are naturally placed in order from morning to evening.
- **Lightweight Conflict Warnings**: Uses hash-mapping logic to detect if multiple tasks (across a single pet or an entire household) are scheduled for the exact same time. Instead of failing the generator, the system safely intercepts the collision and surfaces a readable UI alert to the owner.
- **Automated Recurring Tasks**: Features an automated engine that handles daily and weekly chores. When a `"daily"` or `"weekly"` task is marked complete, the engine deep-clones the event, resets its state to `"pending"`, and automatically increments the `due_date` property utilizing built-in Python `timedelta` native logic.
- **Precise Dataset Filtering**: Contains highly efficient status and pet-name filters that dynamically query and retrieve tasks by either `Completion Status` (Pending vs. Completed) or case-insensitive `Pet Name` to feed accurate data directly to the web client.

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

## Testing PawPal+

To ensure everything runs smoothly, we've included a robust automated test suite using `pytest`. 

To run the test suite, ensure you are in the project root directory and execute:
```bash
python -m pytest
```

### What We Cover
- **Sorting Correctness:** Verifies that tasks provided out of order correctly return in chronologically sorted "HH:MM" format.
- **Recurrence Logic:** Confirms that when a user marks a `"daily"` or `"weekly"` task as complete, the system properly issues a new `"pending"` task for the next due date without user intervention.
- **Conflict Detection:** Ensures that tasks overlapping at the exact same time do not crash the scheduler, but instead gracefully generate distinct warning messages.
- **Task Management and Filtering:** Verifies that adding new tasks correctly increments counts and updating a task's status properly propagates through the system.

**Confidence Level**: ⭐⭐⭐⭐⭐ (5/5 Stars)
Because our unit tests completely execute the happy paths and most likely edge cases for the core algorithms without any errors, the backend logic is highly reliable.
7. Refine UML so it matches what you actually built.
