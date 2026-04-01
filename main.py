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

    # 3. Add Tasks with different times
    # Note: Priorities (lower number usually means higher priority) and timelines
    t1 = Task(name="Morning Walk", task_type="walk", priority=1, duration=30, timeline="morning")
    t2 = Task(name="Feed Luna", task_type="feed", priority=1, duration=10, timeline="morning")
    t3 = Task(name="Afternoon Playtime", task_type="play", priority=3, duration=20, timeline="afternoon")
    t4 = Task(name="Evening Grooming", task_type="groom", priority=2, duration=15, timeline="evening")
    t5 = Task(name="Evening Walk", task_type="walk", priority=1, duration=30, timeline="evening")

    dog.add_task(t1)
    cat.add_task(t2)
    cat.add_task(t3)
    dog.add_task(t4)
    dog.add_task(t5)

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

if __name__ == "__main__":
    main()
