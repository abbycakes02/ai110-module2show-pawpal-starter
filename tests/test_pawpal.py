from pawpal_system import Task, Pet

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
