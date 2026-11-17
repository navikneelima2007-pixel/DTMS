"""
Daily Task Manager
==================
Main entry point for Daily Task Manager.
Runs task_manager.run_app()
"""

from task_manager import (
    FILENAME,
    VALID_PRIORITIES,
    validate_priority,
    validate_date,
    generate_task_id,
    load_tasks,
    save_tasks,
    add_task,
    view_by_priority,
    show_pending,
    complete_task,
    run_app,
)

if __name__ == "__main__":
    run_app()
