from pawpal_system import Task, Pet, Owner, Scheduler

def main():
    # 1. Create an Owner
    owner = Owner(name="Emily")

    # 2. Create at least two Pets
    dog = Pet(
        owner_name="Emily", 
        pet_name="Mochi", 
        pet_type="Dog", 
        age=3, 
        health_notes="Healthy, loves walks"
    )
    cat = Pet(
        owner_name="Emily", 
        pet_name="Luna", 
        pet_type="Cat", 
        age=5, 
        health_notes="Allergic to chicken"
    )
    
    owner.add_pet(dog)
    owner.add_pet(cat)

    # 3. Add Tasks with different times out of order
    # Note: Priorities (lower number usually means higher priority) and timelines
    t1 = Task(name="Morning Walk", task_type="walk", priority=1, duration=30, timeline="morning", time="08:00", recurrence="daily")
    t2 = Task(name="Feed Luna", task_type="feed", priority=1, duration=10, timeline="morning", time="08:00", recurrence="daily")  # Creates an explicit conflict at 08:00
    t3 = Task(name="Afternoon Playtime", task_type="play", priority=3, duration=20, timeline="afternoon", time="14:00")
    t4 = Task(name="Evening Grooming", task_type="groom", priority=2, duration=15, timeline="evening", time="20:00", recurrence="weekly")
    t5 = Task(name="Evening Walk", task_type="walk", priority=1, duration=30, timeline="evening", time="20:00", recurrence="daily") # Creates another conflict at 20:00

    dog.add_task(t1)
    cat.add_task(t3)
    dog.add_task(t5)
    cat.add_task(t2)
    dog.add_task(t4)
    
    # Mark one complete to test status filtering and recurrence
    dog.mark_task_complete(t4)
    dog.mark_task_complete(t1)
    
    print("\n--- Testing Custom Sorting and Filtering ---")
    all_tasks = owner.get_all_tasks()
    
    # Filtering: Pet name
    mochi_tasks = owner.get_tasks_by_pet("Mochi")
    print(f"\nTasks for Mochi (Filtered): {[t.name for t in mochi_tasks]}")

    # Filtering: Status
    pending_tasks = owner.get_tasks_by_status("pending")
    print(f"\nPending Tasks for {owner.name} (Filtered): {[t.name for t in pending_tasks]}")
    
    # Sorting out of order tasks
    print("\nAll Tasks Unsorted:")
    for t in all_tasks:
        print(f" - {t.time} | {t.name}")

    scheduler = Scheduler(owner_time_constraints={"morning": 60, "afternoon": 30, "evening": 60})
    sorted_by_time = scheduler.sort_by_time(all_tasks)

    print("\nAll Tasks Sorted by HH:MM Time:")
    for t in sorted_by_time:
        print(f" - {t.time} | {t.name}")
    print("------------------------------------------\n")
    
    # 4. Initialize Scheduler and generate plan
    # Owner has 60 mins in morning, 30 in afternoon, 60 in evening
    scheduler = Scheduler(owner_time_constraints={"morning": 60, "afternoon": 30, "evening": 60})
    
    plan = scheduler.generate_plan(owner)

    # 5. Print "Today's Schedule"
    print(f"\n{'='*45}")
    print(f" 🐾 TODAY'S SCHEDULE FOR {owner.name.upper()}'s PETS 🐾")
    print(f"{'='*45}")
    
    # Emojis for different times of day
    time_icons = {"morning": "🌅", "afternoon": "☀️", "evening": "🌙"}
    
    # Iterate through the schedule dictionary
    for time_of_day, tasks in plan.schedule.items():
        icon = time_icons.get(time_of_day.lower(), "📅")
        
        # Calculate time used
        total_time = sum(t.duration for t in tasks)
        available_time = scheduler.owner_time_constraints.get(time_of_day.lower(), 0)
        
        print(f"\n{icon} {time_of_day.upper()} (Time used: {total_time}/{available_time} mins)")
        print(f"{'-'*45}")
        
        if not tasks:
            print("   🛋️  No tasks scheduled. Time to relax!")
        else:
            for task in tasks:
                # Add a star for top priority tasks
                priority_marker = "★" if task.priority == 1 else " "
                print(f"   [{task.priority}]{priority_marker} {task.name:<22} ⏱️ {task.duration} mins")
    
    print(f"\n{'='*45}")
    print(" 📝 SUMMARY ")
    print(f"{'='*45}")
    print(plan.explanation)

    if plan.warnings:
        print(f"\n{'='*45}")
        print(" ⚠️  WARNINGS ")
        print(f"{'='*45}")
        for warning in plan.warnings:
            print(f"   - {warning}")

if __name__ == "__main__":
    main()
