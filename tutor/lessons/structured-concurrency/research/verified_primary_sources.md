# Checked against primary sources (2026-09-26)

## openjdk.org/jeps/543 and /jeps/533
- JEP 543: Structured Concurrency. Status: Candidate. Target release: JDK 28. Created 2026/08/05. Proposes to finalize the API.
- JEP 533: Structured Concurrency (Seventh Preview). Status: Closed / Delivered. Release: JDK 27.
- History (as given in JEP 533 and JEP 543): incubator JEP 428 (JDK 19), JEP 437 (JDK 20); preview JEP 453 (JDK 21); re-previews JEP 462 (JDK 22), JEP 480 (JDK 23), JEP 499 (JDK 24), JEP 505 (JDK 25), JEP 525 (JDK 26), JEP 533 (JDK 27).

## docs.python.org/3/library/asyncio-task.html (Python 3.14.7 docs)
- gather: "If return_exceptions is False (default), the first raised exception is immediately propagated to the task that awaits on gather(). Other awaitables in the aws sequence won't be cancelled and will continue to run."
- gather: "A new alternative to create and run tasks concurrently and wait for their completion is asyncio.TaskGroup. TaskGroup provides stronger safety guarantees than gather for scheduling a nesting of subtasks: if a task (or a subtask, a task scheduled by a task) raises an exception, TaskGroup will, while gather will not, cancel the remaining scheduled tasks."
- Task cancellation: "The asyncio components that enable structured concurrency, like asyncio.TaskGroup and asyncio.timeout(), are implemented using cancellation internally and might misbehave if a coroutine swallows asyncio.CancelledError."
- The behaviour was run on Python 3.11.15 (data/runs.txt); the 3.11 docstrings are in verified_python_docstrings.txt.
