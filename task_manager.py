from datetime import datetime
FILE = "tasks.txt"

# Load Tasks
def load_tasks():
    tasks = []

    try:
        file = open(FILE, "r")

        for line in file:
            if line.strip() == "":
                continue

            data = line.strip().split("|")

            if len(data) == 5:
                task = {
                    "id": data[0].strip(),
                    "title": data[1].strip(),
                    "priority": data[2].strip(),
                    "due_date": data[3].strip(),
                    "status": data[4].strip()
                }

                tasks.append(task)

        file.close()

    except FileNotFoundError:
        pass

    return tasks


# Save Tasks
def save_tasks(tasks):
    file = open(FILE, "w")

    for task in tasks:
        file.write(
            task["id"] + " | " +
            task["title"] + " | " +
            task["priority"] + " | " +
            task["due_date"] + " | " +
            task["status"] + "\n"
        )

    file.close()


# Generate Task ID
def generate_id(tasks):
    number = 100

    for task in tasks:
        n = int(task["id"][1:])

        if n > number:
            number = n

    return "T" + str(number + 1)


# Add Task
def add_task(tasks):
    title = input("Title: ").strip()
    priority = input("Priority: ").strip().capitalize()

    if priority not in ["High", "Medium", "Low"]:
        print("Invalid priority. Enter High, Medium or Low.")
        return

    date = input("Due: ").strip()

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    task = {
        "id": generate_id(tasks),
        "title": title,
        "priority": priority,
        "due_date": date,
        "status": "Pending"
    }

    tasks.append(task)
    save_tasks(tasks)

    print("Task added.")
    print(
        task["id"], "|",
        task["title"], "|",
        task["priority"], "|",
        task["due_date"], "|",
        task["status"]
    )


# View Tasks by Priority
def view_by_priority(tasks):
    if len(tasks) == 0:
        print("No tasks found.")
        return

    for priority in ["High", "Medium", "Low"]:
        for task in tasks:
            if task["priority"] == priority:
                print(
                    task["id"], "|",
                    task["title"], "|",
                    task["priority"], "|",
                    task["due_date"]
                )


# Show Pending Tasks
def show_pending(tasks):
    count = 0

    for task in tasks:
        if task["status"].strip().lower() == "pending":
            print(
                task["id"], "|",
                task["title"], "|",
                task["priority"], "|",
                task["due_date"], "|",
                task["status"]
            )

            count += 1

    if count == 0:
        print("No pending tasks. You are all caught up!")


# Complete Task
def complete_task(tasks):
    task_id = input("Task ID: ").strip().upper()

    for task in tasks:
        if task["id"].upper() == task_id:
            task["status"] = "Done"
            save_tasks(tasks)

            count = 0

            for t in tasks:
                if t["status"].strip().lower() == "pending":
                    count += 1

            print(
                "Task", task_id,
                "marked as done. Pending tasks:", count
            )
            return

    print("Task", task_id, "not found.")


# Main Program
def main():
    tasks = load_tasks()

    while True:
        print("\n===== DAILY TASK MANAGER =====")
        print("1. Add")
        print("2. View by priority")
        print("3. Show pending")
        print("4. Complete")
        print("5. Exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            add_task(tasks)

        elif choice == "2":
            view_by_priority(tasks)

        elif choice == "3":
            show_pending(tasks)

        elif choice == "4":
            complete_task(tasks)

        elif choice == "5":
            print("Exiting Daily Task Manager.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
