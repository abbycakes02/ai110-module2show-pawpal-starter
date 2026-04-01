# PawPal+ Project Reflection

## 1. System Design

The 3 core actions the user must be able to take is they should be able to create and manage basic information about the pet, CRUD operations for tasks and the ability to edit the priority and timeline of them, and create a finalized plan with an explanation. 
- We would need a pet object with the attributes for owner name and pet information maybe type of dog, dog name, age and health_notes and have the methods add_task(). remove_task(), get_task() and contains tasks (list[Task]). The Task class would be a separate object where for each task it would have the associated update priority method and update timeline and the attributes name type(walk, feed, groom, eat meds, extracurricular activity), priority, duration, status. The scheduler class would have the methods generate_plan(pet) and returns ordered list of tasks with times and explanation and considers priority, duration, owner time constraints and outputs daily schedule with reasoning.

**a. Initial design**
- added design to mermaid-diagram.png
- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
We had 4 classes in our UML diagram which were Pet, Task, Scheduler, and Plan.

The Pet class acts as the central entity. It stores basic information about the pet and owner, such as name, type, age, and health notes. It also manages a collection of tasks, providing methods to add, remove, and retrieve tasks.

The Task class represents individual activities like feeding, walking, or medication. Each task has attributes such as name, type, priority, duration, status, and timeline. It also includes methods to update priority and timeline, supporting task editing.

The Scheduler class is responsible for generating a structured plan. It takes a Pet object as input and applies logic based on task priority, duration, and constraints to produce an optimized schedule.

Finally, the Plan class represents the output of the system. It contains an ordered list of tasks, along with a schedule and a human-readable explanation of how the plan was generated.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design changed during implementation. I removed update_priority and update_timeline from the Task class because Python Dataclasses allow direct attribute modification.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
My scheduler implements lightweight, exact-time conflict matching rather than checking overlapping durations. 
- Why is that tradeoff reasonable for this scenario?
This decision was made to make the codebase simpler and drastically reduce complex edge-cases like a "20 minute play time" beginning at 1:55PM colliding with a "5 minute feeding" at 2:10PM. For an everyday pet application, pinpointing precise times is the most useful signal an owner will use. Exact time overlap triggers easily readable warnings without failing or halting the app allowing the pet owner to use it strictly as subjective advice rather than hard guardrails.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
