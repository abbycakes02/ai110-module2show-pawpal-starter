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

    def update_priority(self, new_priority: int):
        pass

    def update_timeline(self, new_timeline: str):
        pass

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
        pass

    def remove_task(self, task: Task):
        pass

    def get_task(self) -> List[Task]:
        pass

@dataclass
class Plan:
    """Represents the output of the system: an ordered schedule and explanation."""
    ordered_tasks: List[Task]
    schedule: dict
    explanation: str

class Scheduler:
    """Generates a structured plan taking constraints into account."""
    def __init__(self, owner_time_constraints: int):
        self.owner_time_constraints = owner_time_constraints

    def generate_plan(self, pet: Pet) -> Plan:
        pass
