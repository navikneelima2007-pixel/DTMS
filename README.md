# Daily Task Manager

A Python 3 console task management application that allows users to create, view, track, prioritize, and complete daily tasks with persistent file storage.

---

## 📋 Problem Overview

- **Language:** Python 3
- **Core Concepts:** Lists, Dictionaries, Functions, File Handling, Input Validation
- **Storage:** Persisted to `tasks.txt`
- **Task ID:** Automatically generated starting from `T101`
- **Priorities:** `High`, `Medium`, `Low`
- **Date Format:** `YYYY-MM-DD`
- **Menu Options:**
  1. Add
  2. View by priority
  3. Show pending
  4. Complete
  5. Exit

---

## ⚙️ Bare Minimum Requirements Addressed

1. **Single `.py` solution:** Implemented fully in `task_manager.py` (and callable from `main.py`).
2. **Data Structure:** Each task is stored as a dictionary containing `id`, `title`, `priority`, `due_date`, and `status`, managed inside a master list `tasks`.
3. **Dedicated Functions:**
   - `add_task(tasks, title, priority, due_date, filename="tasks.txt")`
   - `view_by_priority(tasks)`
   - `show_pending(tasks)`
   - `complete_task(tasks, task_id, filename="tasks.txt")`
4. **Validation:**
   - Validates priority strictly (`High`, `Medium`, `Low`).
   - Validates due date format (`YYYY-MM-DD`) and calendar validity.
5. **Persistence:** Loads existing tasks from `tasks.txt` on startup and saves after every state mutation (add, complete).

---

## 🚀 How to Run

### Interactive Console Application
```bash
py -3 task_manager.py
# or
py -3 main.py
```

### Automated Test Suite
```bash
py -3 test_task_manager.py
```

---

## 🧪 Test Cases & Expected Outputs

### Test Case 1: Normal Input
- **Action:** Menu option 1 (Add)
- **Input:**
  - Title: `Submit report`
  - Priority: `High`
  - Due: `2026-10-15`
- **Expected Output:**
  ```text
  Task added.
  T101 | Submit report | High | 2026-10-15 | Pending
  ```

---

### Test Case 2: Boundary / Minimum Input
- **Action:** No tasks in `tasks.txt` -> Menu option 3 (Show pending)
- **Expected Output:**
  ```text
  No pending tasks. You are all caught up!
  ```

---

### Test Case 3: Invalid Input
- **(a) Invalid Priority:**
  - Input: Title: `Pay bill`, Priority: `Urgent`
  - Expected Output: `Invalid priority. Enter High, Medium or Low.`
- **(b) Invalid Date Format:**
  - Input: Title: `Pay bill`, Due: `15-10-2026`
  - Expected Output: `Invalid date. Use YYYY-MM-DD.`
- **(c) Non-existent Task ID:**
  - Input: Option 4 (Complete) with ID `T999`
  - Expected Output: `Task T999 not found.`

---

### Test Case 4: Different Valid Scenario
- **Initial Tasks:**
  - `T101 | Submit report | High | 2026-10-15 | Pending`
  - `T102 | Buy milk | Low | 2026-10-11 | Pending`
  - `T103 | Call bank | Medium | 2026-10-12 | Pending`
- **(a) Menu option 2 (View by priority):**
  - Expected Output:
    ```text
    T101 | Submit report | High | 2026-10-15
    T103 | Call bank | Medium | 2026-10-12
    T102 | Buy milk | Low | 2026-10-11
    ```
- **(b) Menu option 4 (Complete):**
  - Input: `T101`
  - Expected Output:
    ```text
    Task T101 marked as done. Pending tasks: 2
    ```

---

## 📂 File Structure

- [task_manager.py](file:///d:/GSMS/task_manager.py) - Complete standalone solution in Python 3.
- [main.py](file:///d:/GSMS/main.py) - Main entrypoint redirecting to `task_manager.py`.
- [test_task_manager.py](file:///d:/GSMS/test_task_manager.py) - Automated test suite validating all 4 test cases and unit logic.
- `tasks.txt` - File storage for persistent task data.
