import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler, Plan

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Initialize an Owner in session state if it doesn't exist
if "owner" not in st.session_state:
    # Create the default owner and a default pet based on the UI inputs
    default_owner = Owner(name="Jordan")
    default_pet = Pet(
        owner_name="Jordan",
        pet_name="Mochi",
        pet_type="dog",
        age=3,
        health_notes="None"
    )
    default_owner.add_pet(default_pet)
    st.session_state.owner = default_owner

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    timeline = st.selectbox("Timeline", ["morning", "afternoon", "evening"])

col5, col6 = st.columns(2)
with col5:
    task_time = st.time_input("Time", value=None)
with col6:
    recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"])

if st.button("Add task"):
    # Map priority string to integer (1 = high, 2 = medium, 3 = low)
    priority_map = {"high": 1, "medium": 2, "low": 3}
    prio_int = priority_map[priority_str]
    time_str = task_time.strftime("%H:%M") if task_time else "00:00"
    
    # Create the task object
    new_task = Task(
        name=task_title,
        task_type="activity",
        priority=prio_int,
        duration=int(duration),
        timeline=timeline,
        time=time_str,
        recurrence=recurrence
    )
    
    # Assuming the first pet is selected for now
    st.session_state.owner.pets[0].add_task(new_task)
    st.success(f"Added '{task_title}' to {st.session_state.owner.pets[0].pet_name}'s tasks!")

all_tasks = st.session_state.owner.get_tasks_by_status("pending")
if all_tasks:
    st.write(f"Current pending tasks for {st.session_state.owner.pets[0].pet_name}:")
    # Display tasks elegantly from objects using the internal filtering capability
    task_data = [{"Name": t.name, "Time": t.time, "Duration": f"{t.duration}m", "Priority": t.priority, "Timeline": t.timeline.capitalize(), "Recurrence": t.recurrence.capitalize()} for t in all_tasks]
    st.table(task_data)
else:
    st.info("No pending tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generates a structured plan taking constraints into account.")

if st.button("Generate schedule"):
    if not all_tasks:
        st.warning("Please add some tasks first!")
    else:
        # Define constraints (e.g. from UI sliders if you want, or hardcoded for now)
        constraints = {"morning": 60, "afternoon": 60, "evening": 60}
        scheduler = Scheduler(owner_time_constraints=constraints)
        
        # Generate the plan
        plan = scheduler.generate_plan(st.session_state.owner)
        
        st.success("Plan generated successfully!")
        
        # Display the explanation
        st.markdown(f"### Planner Summary \n> {plan.explanation}")
        
        # Output any conflict detection alerts straight into the UI 
        if getattr(plan, "warnings", []):
            st.markdown("#### 🚨 Scheduling Warnings")
            for w in plan.warnings:
                st.warning(w)

        # Display schedule
        st.markdown("### 🐾 Daily Breakdown")
        for time_period, tasks in plan.schedule.items():
            st.divider()
            st.subheader(f"{time_period.capitalize()}")
            if not tasks:
                st.write("*No tasks scheduled.*")
            else:
                # Neatly utilize the time sorting logic built previously in the backend!
                sorted_timeline_tasks = scheduler.sort_by_time(tasks)
                for t in sorted_timeline_tasks:
                    star = "★" if t.priority == 1 else "▪"
                    st.write(f"**{star} {t.time} - {t.name}**")
                    st.caption(f"⏱ *{t.duration} min* | 🔄 *{t.recurrence.title()}*")
