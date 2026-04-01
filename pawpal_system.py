from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class Task:
    """Represents an individual pet care activity."""
    name: str
    task_type: str  # e.g., walk, feed, groom, eat meds, extracurricular activity
    priority: int
    duration: int
    timeline: str
    status: str = "pending"

    def mark_complete(self):
        """Marks the task as completed."""
        self.status = "completed"

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

@dataclass
class Plan:
    """Represents the output of the system: an ordered schedule and explanation."""
    ordered_tasks: List[Task]
    schedule: dict
    explanation: str

class Scheduler:
    """Generates a structured plan taking constraints into account."""
    def __init__(self, owner_time_constraints: dict):
        # e.g., {"morning": 60, "afternoon": 30, "evening": 60}
        self.owner_time_constraints = owner_time_constraints

    def generate_plan(self, owner: Owner) -> Plan:
        """Generates an optimized daily schedule based on time constraints and task priorities."""
        all_tasks = owner.get_all_tasks()
        
        # Sort by priority: 1 is highest priority
        sorted_tasks = sorted(all_tasks, key=lambda t: t.priority)
        
        scheduled_tasks = []
        schedule = {"morning": [], "afternoon": [], "evening": []}
        time_used = {"morning": 0, "afternoon": 0, "evening": 0}
        
        # Simple scheduling logic
        for task in sorted_tasks:
            time_of_day = task.timeline.lower()
            if time_of_day in self.owner_time_constraints:
                if time_used[time_of_day] + task.duration <= self.owner_time_constraints[time_of_day]:
                    scheduled_tasks.append(task)
                    schedule[time_of_day].append(task)
                    time_used[time_of_day] += task.duration

        explanation = (
            f"Generated plan for {owner.name}'s pets. "
            f"Scheduled {len(scheduled_tasks)} out of {len(all_tasks)} tasks "
            f"based on time available: {self.owner_time_constraints}."
        )

        return Plan(
            ordered_tasks=scheduled_tasks,
            schedule=schedule,
            explanation=explanation
        )
