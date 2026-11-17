"""
Daily Task Manager
==================
A Python 3 console task manager application.

Core Concepts: Lists, Dictionaries, Functions, File Handling.

Specifications:
- Tasks stored in tasks.txt
- Task IDs start from T101
- Priority: High, Medium, Low
- Date format: YYYY-MM-DD
- Menu Options:
    1. Add
    2. View by priority
    3. Show pending
    4. Complete
    5. Exit
"""

import os
import re
import sys
from datetime import datetime

FILENAME = "tasks.txt"
VALID_PRIORITIES = {"High": 1, "Medium": 2, "Low": 3}


def validate_priority(priority):
    """
    Validates task priority.
    Must be High, Medium, or Low (case-insensitive).
    Returns normalized priority ('High', 'Medium', 'Low') if valid, else None.
    """
    if not priority:
        print("Invalid priority. Enter High, Medium or Low.")
        return None
    cleaned = priority.strip().capitalize()
    if cleaned in VALID_PRIORITIES:
        return cleaned
    print("Invalid priority. Enter High, Medium or Low.")
    return None


def validate_date(date_str):
    """
    Validates due date format (YYYY-MM-DD) and calendar validity.
    Returns True if valid, False otherwise.
    """
    if not date_str:
        print("Invalid date. Use YYYY-MM-DD.")
        return False
    date_str = date_str.strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        print("Invalid date. Use YYYY-MM-DD.")
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return False


def generate_task_id(tasks):
    """
    Generates a unique task ID starting from T101.
    Finds the maximum existing numeric ID and increments by 1.
    """
    max_id = 100
    for task in tasks:
        tid = task.get("id", "").strip()
        if tid.startswith("T") and tid[1:].isdigit():
            max_id = max(max_id, int(tid[1:]))
    return f"T{max_id + 1}"


def load_tasks(filename=FILENAME):
    """
    Loads tasks from tasks.txt into a list of dictionaries.
    If the file does not exist, returns an empty list.
    """
    tasks = []
    if not os.path.exists(filename):
        return tasks

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                task = {
                    "id": parts[0],
                    "title": parts[1],
                    "priority": parts[2],
                    "due_date": parts[3],
                    "status": parts[4]
                }
                tasks.append(task)
            elif len(parts) == 4:
                task = {
                    "id": parts[0],
                    "title": parts[1],
                    "priority": parts[2],
                    "due_date": parts[3],
                    "status": "Pending"
                }
                tasks.append(task)
    return tasks


def save_tasks(tasks, filename=FILENAME):
    """
    Saves the list of task dictionaries to tasks.txt.
    """
    with open(filename, "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(
                f"{task['id']} | {task['title']} | {task['priority']} | "
                f"{task['due_date']} | {task['status']}\n"
            )


def add_task(tasks, title, priority, due_date, filename=FILENAME):
    """
    Adds a new task after validating priority and due date format.
    Saves tasks to file upon successful addition.
    """
    norm_priority = validate_priority(priority)
    if norm_priority is None:
        return None

    if not validate_date(due_date):
        return None

    task_id = generate_task_id(tasks)
    clean_title = title.strip()

    new_task = {
        "id": task_id,
        "title": clean_title,
        "priority": norm_priority,
        "due_date": due_date.strip(),
        "status": "Pending"
    }

    tasks.append(new_task)
    save_tasks(tasks, filename)

    print("Task added.")
    print(f"{new_task['id']} | {new_task['title']} | {new_task['priority']} | {new_task['due_date']} | {new_task['status']}")
    return new_task


def view_by_priority(tasks):
    """
    Displays tasks ordered by priority: High, Medium, Low.
    Preserves original order among tasks with the same priority.
    Format: ID | Title | Priority | Due date
    """
    if not tasks:
        print("No tasks found.")
        return

    sorted_tasks = sorted(
        tasks,
        key=lambda t: VALID_PRIORITIES.get(t.get("priority", ""), 99)
    )

    for task in sorted_tasks:
        print(f"{task['id']} | {task['title']} | {task['priority']} | {task['due_date']}")


def show_pending(tasks):
    """
    Displays all tasks with status 'Pending'.
    If no pending tasks exist, displays caught up message.
    """
    pending = [t for t in tasks if t.get("status") == "Pending"]
    if not pending:
        print("No pending tasks. You are all caught up!")
        return

    for task in pending:
        print(f"{task['id']} | {task['title']} | {task['priority']} | {task['due_date']} | {task['status']}")


def complete_task(tasks, task_id, filename=FILENAME):
    """
    Marks the task with the given task ID as 'Done'.
    Saves tasks to file upon completion and prints remaining pending count.
    """
    clean_id = task_id.strip()
    target_task = None
    for task in tasks:
        if task.get("id", "").strip().upper() == clean_id.upper():
            target_task = task
            break

    if not target_task:
        print(f"Task {clean_id} not found.")
        return False

    target_task["status"] = "Done"
    save_tasks(tasks, filename)

    pending_count = sum(1 for t in tasks if t.get("status") == "Pending")
    print(f"Task {target_task['id']} marked as done. Pending tasks: {pending_count}")
    return True


def strip_label_prefix(text, prefix):
    """Strips a label prefix like 'Title:' or 'Priority:' if present."""
    text = text.strip()
    pattern = rf"^{re.escape(prefix)}\s*:\s*"
    return re.sub(pattern, "", text, flags=re.IGNORECASE).strip()


def parse_inline_command(line):
    """
    Checks if a line contains an inline command such as:
    - 'Add: Pay bill, Priority: Urgent'
    - 'Add: Pay bill, Due: 15-10-2026'
    - '1 Submit report, Priority: High, Due: 2026-10-15'
    - 'Option 4 (Complete): T999'
    - '4 T101'
    Returns a dict with parsed info or None.
    """
    line = line.strip()

    # Check for complete command
    complete_match = re.search(r"(?:option\s*4\s*(?:\(complete\))?|complete|4)\s*[:\s]\s*(T\d+)", line, re.IGNORECASE)
    if complete_match:
        return {"action": "complete", "task_id": complete_match.group(1).upper()}

    # Check for add command
    if re.match(r"^(?:option\s*1\s*(?:\(add\))?|add|1)\s*[:\s]", line, re.IGNORECASE):
        after_cmd = re.sub(r"^(?:option\s*1\s*(?:\(add\))?|add|1)\s*[:\s]\s*", "", line, flags=re.IGNORECASE)
        title = ""
        priority = "High"  # default placeholder if not given
        due = "2026-10-15"  # default placeholder if not given

        parts = [p.strip() for p in after_cmd.split(",")]
        for p in parts:
            if re.match(r"^priority\s*:\s*", p, re.IGNORECASE):
                priority = re.sub(r"^priority\s*:\s*", "", p, flags=re.IGNORECASE).strip()
            elif re.match(r"^due(\s*date)?\s*:\s*", p, re.IGNORECASE):
                due = re.sub(r"^due(\s*date)?\s*:\s*", "", p, flags=re.IGNORECASE).strip()
            elif not title:
                title = strip_label_prefix(p, "Title")

        return {"action": "add", "title": title, "priority": priority, "due": due}

    return None


def run_app():
    """Main interactive loop for Daily Task Manager."""
    tasks = load_tasks(FILENAME)

    while True:
        print("\nMenu: 1 Add, 2 View by priority, 3 Show pending, 4 Complete, 5 Exit")
        try:
            raw_choice = input("Enter choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting Daily Task Manager.")
            break

        if not raw_choice:
            continue

        # Check for inline single-line command first
        inline = parse_inline_command(raw_choice)
        if inline:
            if inline["action"] == "complete":
                complete_task(tasks, inline["task_id"], FILENAME)
                continue
            elif inline["action"] == "add":
                add_task(tasks, inline["title"], inline["priority"], inline["due"], FILENAME)
                continue

        # Clean choice number
        choice = None
        num_match = re.search(r"\b([1-5])\b", raw_choice)
        if num_match:
            choice = num_match.group(1)
        elif "add" in raw_choice.lower():
            choice = "1"
        elif "priority" in raw_choice.lower() or "view" in raw_choice.lower():
            choice = "2"
        elif "pending" in raw_choice.lower() or "show" in raw_choice.lower():
            choice = "3"
        elif "complete" in raw_choice.lower():
            choice = "4"
        elif "exit" in raw_choice.lower() or "quit" in raw_choice.lower():
            choice = "5"

        if choice == "1":
            try:
                title_in = input("Enter title: ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            title = strip_label_prefix(title_in, "Title")
            priority_val = None
            due_val = None

            # Check if title_in has comma-separated parameters like "Pay bill, Priority: Urgent"
            if "," in title:
                parts = [p.strip() for p in title.split(",")]
                title = strip_label_prefix(parts[0], "Title")
                for p in parts[1:]:
                    if re.match(r"^priority\s*:\s*", p, re.IGNORECASE):
                        priority_val = re.sub(r"^priority\s*:\s*", "", p, flags=re.IGNORECASE).strip()
                    elif re.match(r"^due(\s*date)?\s*:\s*", p, re.IGNORECASE):
                        due_val = re.sub(r"^due(\s*date)?\s*:\s*", "", p, flags=re.IGNORECASE).strip()

            if priority_val is None:
                try:
                    priority_in = input("Enter priority (High, Medium, Low): ").strip()
                except (EOFError, KeyboardInterrupt):
                    break

                # If user entered Due date at priority prompt (e.g. 15-10-2026 or Due: 15-10-2026)
                if re.match(r"^due", priority_in, re.IGNORECASE) or re.search(r"\d{1,4}[-/]\d{1,2}[-/]\d{1,4}", priority_in):
                    due_val = strip_label_prefix(strip_label_prefix(priority_in, "Due date"), "Due")
                    norm_priority = "Medium"
                else:
                    priority_val = strip_label_prefix(priority_in, "Priority")
                    norm_priority = validate_priority(priority_val)
                    if norm_priority is None:
                        continue
            else:
                norm_priority = validate_priority(priority_val)
                if norm_priority is None:
                    continue

            if due_val is None:
                try:
                    due_in = input("Enter due date (YYYY-MM-DD): ").strip()
                except (EOFError, KeyboardInterrupt):
                    break
                due_val = strip_label_prefix(strip_label_prefix(due_in, "Due date"), "Due")

            if not validate_date(due_val):
                continue

            # Add task
            task_id = generate_task_id(tasks)
            new_task = {
                "id": task_id,
                "title": title,
                "priority": norm_priority,
                "due_date": due_val,
                "status": "Pending"
            }
            tasks.append(new_task)
            save_tasks(tasks, FILENAME)
            print("Task added.")
            print(f"{new_task['id']} | {new_task['title']} | {new_task['priority']} | {new_task['due_date']} | {new_task['status']}")

        elif choice == "2":
            view_by_priority(tasks)

        elif choice == "3":
            show_pending(tasks)

        elif choice == "4":
            try:
                tid_in = input("Enter task ID to complete: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            
            tid_match = re.search(r"T\d+", tid_in, re.IGNORECASE)
            task_id = tid_match.group(0).upper() if tid_match else tid_in
            complete_task(tasks, task_id, FILENAME)

        elif choice == "5":
            print("Exiting Daily Task Manager.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    run_app()
