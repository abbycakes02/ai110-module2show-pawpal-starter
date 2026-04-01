from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler

def test_task_completion():
    """Verify that calling mark_complete() actually changes the task's status."""
    task = Task(
        name="Morning Walk",
        task_type="walk",
        priority=1,
        duration=30,
        timeline="morning"
    )
    
    assert task.status == "pending"
    task.mark_complete()
    assert task.status == "completed"

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(
        owner_name="Emily",
        pet_name="Mochi",
        pet_type="Dog",
        age=3,
        health_notes="Healthy"
    )
    
    assert len(pet.get_tasks()) == 0
    
    task = Task(
        name="Morning Walk",
        task_type="walk",
        priority=1,
        duration=30,
        timeline="morning"
    )
    
    pet.add_task(task)
    
    assert len(pet.get_tasks()) == 1
    assert pet.get_tasks()[0] == task

def test_scheduler_sorting():
    """Verify tasks are returned in chronological order"""
    scheduler = Scheduler({"morning": 60})
    
    tasks = [
        Task("Lunch", "feed", 2, 10, "afternoon", time="13:00"),
        Task("Morning Walk", "walk", 1, 30, "morning", time="08:30"),
        Task("Late Night", "potty", 3, 5, "evening", time="23:15"),
        Task("Breakfast", "feed", 1, 5, "morning", time="07:00")
    ]
    
    sorted_tasks = scheduler.sort_by_time(tasks)
    
    assert sorted_tasks[0].name == "Breakfast"
    assert sorted_tasks[1].name == "Morning Walk"
    assert sorted_tasks[2].name == "Lunch"
    assert sorted_tasks[3].name == "Late Night"

def test_recurring_tasks():
    """Confirm that marking a daily task complete creates a new task for the following day"""
    base_date = date.today()
    
    # Happy path: Daily recurrence
    daily_task = Task("Meds", "health", 1, 5, "morning", time="09:00", recurrence="daily", due_date=base_date)
    new_daily = daily_task.mark_complete()
    assert daily_task.status == "completed"
    assert new_daily is not None
    assert new_daily.status == "pending"
    assert new_daily.due_date == base_date + timedelta(days=1)
    
def test_scheduler_conflict_detection():
    """Verify that the Scheduler flags duplicate times"""
    scheduler = Scheduler({"morning": 100})
    
    # Conflict tasks at the exact same time
    conflict_tasks = [
        Task("Feed Dog", "feed", 1, 10, "morning", time="08:00"),
        Task("Walk Dog", "walk", 2, 20, "morning", time="08:00"),
        Task("Feed Cat", "feed", 1, 5, "morning", time="08:00"),
        Task("Groom", "groom", 3, 30, "evening", time="19:00")
    ]
    
    warnings = scheduler.check_time_conflicts(conflict_tasks)
    
    assert len(warnings) == 1  # 1 cluster of conflicts
    assert "08:00" in warnings[0]
    assert "Feed Dog" in warnings[0]
    assert "Walk Dog" in warnings[0]
    assert "Feed Cat" in warnings[0]

