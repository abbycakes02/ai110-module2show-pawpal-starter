from typing import List, Optional
from dataclasses import dataclass, field
from datetime import date, timedelta
import copy

@dataclass
class Task:
    """Represents an individual pet care activity."""
    name: str
    task_type: str  # e.g., walk, feed, groom, eat meds, extracurricular activity
    priority: int
    duration: int
    timeline: str
    time: str = "00:00"  # HH:MM format
    status: str = "pending"
    recurrence: str = "none"  # "none", "daily", "weekly"
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> Optional['Task']:
        """Marks the task as completed. If recurring, returns a new pending task for the next occurrence."""
        self.status = "completed"
        
        if self.recurrence.lower() == "daily":
            new_task = copy.deepcopy(self)
            new_task.status = "pending"
            if new_task.due_date:
                new_task.due_date += timedelta(days=1)
            return new_task
            
        elif self.recurrence.lower() == "weekly":
            new_task = copy.deepcopy(self)
            new_task.status = "pending"
            if new_task.due_date:
                new_task.due_date += timedelta(days=7)
            return new_task
            
        return None

@dataclass
class Pet:
    """Stores basic information about the pet and manages its tasks."""
    owner_name: str
    pet_name: str
    pet_type: str
    age: int
    health_notes: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Adds a new task to the pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Removes a given task from the pet's task list if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)

    def mark_task_complete(self, task: Task):
        """Marks a specific task as complete and handles recurrence."""
        if task in self.tasks:
            new_task = task.mark_complete()
            if new_task:
                self.add_task(new_task)

    def get_tasks(self) -> List[Task]:
        """Returns all tasks associated with this pet."""
        return self.tasks

@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Adds a new pet to the owner's profile."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Retrieves and consolidates tasks across all pets belonging to the owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_tasks_by_pet(self, pet_name: str) -> List[Task]:
        """
        Retrieves a filtered list of all tasks assigned specifically to the pet specified.

        Args:
            pet_name (str): The name of the pet to check tasks for (case-insensitive).

        Returns:
            List[Task]: A list containing only tasks associated with the pet, or an empty list if none match.
        """
        for pet in self.pets:
            if pet.pet_name.lower() == pet_name.lower():
                return pet.get_tasks()
        return []

    def get_tasks_by_status(self, status: str) -> List[Task]:
        """
        Retrieves a filtered list of an owner's combined tasks across all pets, based on the task's completion status.

        Args:
            status (str): The status to filter by, typically "pending" or "completed" (case-insensitive).

        Returns:
            List[Task]: A list containing all tasks across every pet that match the requested status.
        """
        return [task for task in self.get_all_tasks() if task.status.lower() == status.lower()]

@dataclass
class Plan:
    """Represents the output of the system: an ordered schedule and explanation."""
    ordered_tasks: List[Task]
    schedule: dict
    explanation: str
    conflicts: List[Task] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

class Scheduler:
    """Generates a structured plan taking constraints into account."""
    def __init__(self, owner_time_constraints: dict):
        # e.g., {"morning": 60, "afternoon": 30, "evening": 60}
        self.owner_time_constraints = owner_time_constraints

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sorts a given list of Task objects chronologically using their string 'time' attribute.

        Args:
            tasks (List[Task]): A list of tasks to sort.

        Returns:
            List[Task]: A new list containing the tasks sorted by time in "HH:MM" 24-hour format.
        """
        # A simple lambda lambda t: t.time is enough for "HH:MM" 24-hour formats
        return sorted(tasks, key=lambda t: t.time)

    def check_time_conflicts(self, tasks: List[Task]) -> List[str]:
        """
        Performs a lightweight scan over a list of Tasks to determine if any share the same precise time attribute.

        Logs a human-readable string warning in the application warning array rather than raising exceptions.

        Args:
            tasks (List[Task]): The active/pending list of tasks.

        Returns:
            List[str]: A list of warning messages for each unique overlapping string timestamp.
        """
        warnings = []
        time_map = {}
        for task in tasks:
            if task.time not in time_map:
                time_map[task.time] = []
            time_map[task.time].append(task.name)
            
        for time, task_names in time_map.items():
            if len(task_names) > 1:
                warnings.append(f"Multiple tasks scheduled at {time} ({', '.join(task_names)}).")
        return warnings

    def generate_plan(self, owner: Owner) -> Plan:
        """Generates an optimized daily schedule based on time constraints and task priorities."""
        # Filter out completed tasks so we only schedule pending ones
        pending_tasks = owner.get_tasks_by_status("pending")
        
        # Perform lightweight conflict detection
        time_warnings = self.check_time_conflicts(pending_tasks)
        
        # Sort tasks by timeline order, then by priority (1 is highest), then by duration (shortest first)
        timeline_order = {"morning": 1, "afternoon": 2, "evening": 3}
        sorted_tasks = sorted(pending_tasks, key=lambda t: (timeline_order.get(t.timeline.lower(), 4), t.priority, t.duration))
        
        scheduled_tasks = []
        conflicts = []
        schedule = {"morning": [], "afternoon": [], "evening": []}
        time_used = {"morning": 0, "afternoon": 0, "evening": 0}
        
        # Logic with basic conflict detection
        for task in sorted_tasks:
            time_of_day = task.timeline.lower()
            if time_of_day in self.owner_time_constraints:
                if time_used[time_of_day] + task.duration <= self.owner_time_constraints[time_of_day]:
                    scheduled_tasks.append(task)
                    schedule[time_of_day].append(task)
                    time_used[time_of_day] += task.duration

                    # Reset recurring task status implicitly, but for this step we'll just handle it as not completed
                else:
                    conflicts.append(task)
            else:
                conflicts.append(task)

        explanation = (
            f"Generated plan for {owner.name}'s pets. "
            f"Scheduled {len(scheduled_tasks)} out of {len(pending_tasks)} pending tasks "
            f"based on time available: {self.owner_time_constraints}. "
        )
        if conflicts:
            explanation += f"Could not fit {len(conflicts)} tasks due to time constraints. "

        return Plan(
            ordered_tasks=scheduled_tasks,
            schedule=schedule,
            explanation=explanation,
            conflicts=conflicts,
            warnings=time_warnings
        )
