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
My scheduler considers the owner's total available time per period (morning, afternoon, evening), the numerical priority of the task, the task's individual duration, and exact chronological "time" attributes.
- How did you decide which constraints mattered most?
I decided that the owner's time block capacity mattered most because it's a strict physical constraint. Priority was implemented as the primary sorting mechanism to ensure critical tasks like feeding happen before play times, and duration acts as a tie-breaker so we can pack as many smaller tasks as possible into the remaining time.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
My scheduler implements lightweight, exact-time conflict matching rather than checking overlapping durations. 
- Why is that tradeoff reasonable for this scenario?
This decision was made to make the codebase simpler and drastically reduce complex edge-cases like a "20 minute play time" beginning at 1:55PM colliding with a "5 minute feeding" at 2:10PM. For an everyday pet application, pinpointing precise times is the most useful signal an owner will use. Exact time overlap triggers easily readable warnings without failing or halting the app allowing the pet owner to use it strictly as subjective advice rather than hard guardrails.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I completely utilized VS Code Copilot, notably its Agent Mode, Inline Chat, and the `#codebase` feature context variables. Using separate chat sessions for different phases (e.g. Design, Algorithms, Testing) was immensely helpful because it kept Copilot's context entirely focused on that precise goal.
- What kinds of prompts or questions were most helpful?
Prompts like "@workspace #codebase I need to write pytest test functions... What are the most important edge cases?" gave me exactly what I wanted. Direct, architectural questions returned the cleanest structure.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
When implementing Conflict Detection, Copilot initially drafted an incredibly complex overlap calculator validating every minute across a time duration format. I rejected this.
- How did you evaluate or verify what the AI suggested?
I verified that it bloated my design. To keep my system design clean, I commanded the AI to create a "lightweight" match dictionary instead, which only warns on exact string collisions (e.g., both tasks starting right at "08:00").

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
Sorting correctly by chronological time, `timedelta` duplication logic for Recurring Tasks, Conflict Detection matching, and the Owner-level dataset filtering logic.
- Why were these tests important?
They execute my exact edge-cases and happy-paths, ensuring my Streamlit frontend doesn't crash when passing real variables.

**b. Confidence**

- How confident are you that your scheduler works correctly?
5/5 stars (Extremely Confident). 
- What edge cases would you test next if you had more time?
Overnight recurring tasks that span across midnight causing dates to collide, or dynamically shrinking the owner's available timeframe on weekends.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Bridging my backend python code directly to my web-based Streamlit UI components successfully with real-time feedback.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
Connecting the application to a true Database instead of just holding `session_state` variables so actual historical pet activity is tracked forever.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned an incredible amount about being the "lead architect" when collaborating with powerful AI tools. I did a good amount of work manually dictating the logic, architecture spacing, and UX, but I specifically directed the AI to act as my assistant developer. Using AI for rapid syntax lookup, drafting test edge-cases, and managing boilerplate code allowed me to stay heavily optimized and in control over my codebase.
