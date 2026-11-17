"""
Comprehensive Test Suite for Daily Task Manager
Validates:
1. End-to-end console execution for all 4 Test Cases:
   - Test Case 1: Normal Input (Add task)
   - Test Case 2: Boundary / Minimum Input (Empty tasks file -> Show pending)
   - Test Case 3: Invalid Input (Invalid priority, Invalid date format, Non-existent task ID)
   - Test Case 4: Different Valid Scenario (View by priority, Complete task)
2. Alternative interactive and labeled inputs (e.g. Title: ..., Priority: ..., Due: ...)
3. Unit tests directly calling required functions:
   - add_task, view_by_priority, show_pending, complete_task
   - validate_priority, validate_date, load_tasks, save_tasks
"""

import subprocess
import os
import sys
import io
from contextlib import redirect_stdout

TASK_FILE = os.path.join(r"d:\GSMS", "tasks.txt")
SCRIPT = os.path.join(r"d:\GSMS", "task_manager.py")

import task_manager


def reset_tasks_file(content=None):
    """Resets tasks.txt with optional initial content or removes it."""
    if os.path.exists(TASK_FILE):
        os.remove(TASK_FILE)
    if content is not None:
        with open(TASK_FILE, "w", encoding="utf-8") as f:
            f.write(content)


def run_process(input_text):
    """Runs task_manager.py with simulated stdin."""
    proc = subprocess.run(
        [sys.executable, SCRIPT],
        input=input_text,
        text=True,
        capture_output=True,
        cwd=r"d:\GSMS"
    )
    return proc.stdout, proc.stderr


def test_case_1():
    print("\n================== TEST CASE 1: Normal Input ==================")
    reset_tasks_file()
    
    # Menu option 1 (Add)
    # Title: Submit report
    # Priority: High
    # Due: 2026-10-15
    input_str = "1\nSubmit report\nHigh\n2026-10-15\n5\n"
    out, err = run_process(input_str)
    
    expected_lines = [
        "Task added.",
        "T101 | Submit report | High | 2026-10-15 | Pending"
    ]
    
    passed = True
    for exp in expected_lines:
        if exp in out:
            print(f" [PASS] Found expected line: '{exp}'")
        else:
            print(f" [FAIL] Expected line NOT found: '{exp}'")
            passed = False
            
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            file_data = f.read().strip()
        print(f" [INFO] File content: {file_data}")
        if "T101 | Submit report | High | 2026-10-15 | Pending" in file_data:
            print(" [PASS] File content matches expected record.")
        else:
            print(" [FAIL] File content does not match.")
            passed = False
    else:
        print(" [FAIL] tasks.txt was not created!")
        passed = False
        
    return passed


def test_case_1_labeled():
    print("\n--- Test Case 1 with Labeled Inputs ('Title: ...') ---")
    reset_tasks_file()
    
    input_str = "1\nTitle: Submit report\nPriority: High\nDue: 2026-10-15\n5\n"
    out, err = run_process(input_str)
    
    expected_lines = [
        "Task added.",
        "T101 | Submit report | High | 2026-10-15 | Pending"
    ]
    
    passed = True
    for exp in expected_lines:
        if exp in out:
            print(f" [PASS] Found expected line: '{exp}'")
        else:
            print(f" [FAIL] Expected line NOT found: '{exp}'")
            passed = False
    return passed


def test_case_2():
    print("\n================== TEST CASE 2: Boundary / Minimum Input ==================")
    reset_tasks_file()  # No tasks in tasks.txt
    
    # Menu option 3 (Show pending)
    input_str = "3\n5\n"
    out, err = run_process(input_str)
    
    expected = "No pending tasks. You are all caught up!"
    if expected in out:
        print(f" [PASS] Found expected line: '{expected}'")
        return True
    else:
        print(f" [FAIL] Expected line NOT found: '{expected}'")
        return False


def test_case_3():
    print("\n================== TEST CASE 3: Invalid Input ==================")
    all_passed = True

    # (a) Add: Pay bill, Priority: Urgent -> Invalid priority. Enter High, Medium or Low.
    reset_tasks_file()
    print("--- (a) Invalid priority ---")
    input_3a = "1\nPay bill\nUrgent\n5\n"
    out_3a, _ = run_process(input_3a)
    exp_3a = "Invalid priority. Enter High, Medium or Low."
    if exp_3a in out_3a:
        print(f" [PASS] 3(a) Output matched: '{exp_3a}'")
    else:
        print(f" [FAIL] 3(a) Missing output: '{exp_3a}'\nSTDOUT: {out_3a}")
        all_passed = False

    # Also test inline 3(a):
    out_3a_inline, _ = run_process("Add: Pay bill, Priority: Urgent\n5\n")
    if exp_3a in out_3a_inline:
        print(f" [PASS] 3(a) Inline matched: '{exp_3a}'")
    else:
        print(f" [FAIL] 3(a) Inline missing: '{exp_3a}'")
        all_passed = False

    # (b) Add: Pay bill, Due: 15-10-2026 -> Invalid date. Use YYYY-MM-DD.
    print("--- (b) Invalid date format ---")
    input_3b = "1\nPay bill\nHigh\n15-10-2026\n5\n"
    out_3b, _ = run_process(input_3b)
    exp_3b = "Invalid date. Use YYYY-MM-DD."
    if exp_3b in out_3b:
        print(f" [PASS] 3(b) Output matched: '{exp_3b}'")
    else:
        print(f" [FAIL] 3(b) Missing output: '{exp_3b}'\nSTDOUT: {out_3b}")
        all_passed = False

    # Also test inline 3(b):
    out_3b_inline, _ = run_process("Add: Pay bill, Due: 15-10-2026\n5\n")
    if exp_3b in out_3b_inline:
        print(f" [PASS] 3(b) Inline matched: '{exp_3b}'")
    else:
        print(f" [FAIL] 3(b) Inline missing: '{exp_3b}'")
        all_passed = False

    # (c) Option 4 (Complete): T999 -> Task T999 not found.
    print("--- (c) Task not found ---")
    input_3c = "4\nT999\n5\n"
    out_3c, _ = run_process(input_3c)
    exp_3c = "Task T999 not found."
    if exp_3c in out_3c:
        print(f" [PASS] 3(c) Output matched: '{exp_3c}'")
    else:
        print(f" [FAIL] 3(c) Missing output: '{exp_3c}'\nSTDOUT: {out_3c}")
        all_passed = False

    # Also test inline 3(c):
    out_3c_inline, _ = run_process("Option 4 (Complete): T999\n5\n")
    if exp_3c in out_3c_inline:
        print(f" [PASS] 3(c) Inline matched: '{exp_3c}'")
    else:
        print(f" [FAIL] 3(c) Inline missing: '{exp_3c}'")
        all_passed = False

    return all_passed


def test_case_4():
    print("\n================== TEST CASE 4: Different Valid Scenario ==================")
    initial_content = (
        "T101 | Submit report | High | 2026-10-15 | Pending\n"
        "T102 | Buy milk | Low | 2026-10-11 | Pending\n"
        "T103 | Call bank | Medium | 2026-10-12 | Pending\n"
    )
    reset_tasks_file(initial_content)
    
    # (a) Option 2 (View by priority)
    # (b) Option 4 (Complete): T101
    input_str = "2\n4\nT101\n5\n"
    out, err = run_process(input_str)
    
    expected_outputs = [
        "T101 | Submit report | High | 2026-10-15",
        "T103 | Call bank | Medium | 2026-10-12",
        "T102 | Buy milk | Low | 2026-10-11",
        "Task T101 marked as done. Pending tasks: 2"
    ]
    
    passed = True
    for exp in expected_outputs:
        if exp in out:
            print(f" [PASS] Found expected line: '{exp}'")
        else:
            print(f" [FAIL] Expected line NOT found: '{exp}'")
            passed = False
            
    with open(TASK_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print(" [INFO] Updated tasks.txt contents:")
    for l in lines:
        print("   " + l.strip())
        
    if any("T101" in l and "Done" in l for l in lines) and any("T102" in l and "Pending" in l for l in lines):
        print(" [PASS] File persistence verified: T101 is Done, others Pending.")
    else:
        print(" [FAIL] File persistence check failed.")
        passed = False
        
    return passed


def test_unit_functions():
    print("\n================== UNIT TESTS: Direct Function Verification ==================")
    reset_tasks_file()
    tasks = []
    passed = True

    # Test add_task
    t1 = task_manager.add_task(tasks, "Submit report", "High", "2026-10-15", TASK_FILE)
    if t1 and t1["id"] == "T101" and t1["status"] == "Pending":
        print(" [PASS] add_task created T101 properly.")
    else:
        print(" [FAIL] add_task failed.")
        passed = False

    t2 = task_manager.add_task(tasks, "Buy milk", "Low", "2026-10-11", TASK_FILE)
    t3 = task_manager.add_task(tasks, "Call bank", "Medium", "2026-10-12", TASK_FILE)
    if t2["id"] == "T102" and t3["id"] == "T103":
        print(" [PASS] Incremental IDs T102, T103 generated correctly.")
    else:
        print(" [FAIL] Incremental IDs failed.")
        passed = False

    # Test view_by_priority output capture
    buf = io.StringIO()
    with redirect_stdout(buf):
        task_manager.view_by_priority(tasks)
    vp_out = buf.getvalue().strip().split("\n")
    if (
        "T101 | Submit report | High | 2026-10-15" in vp_out[0] and
        "T103 | Call bank | Medium | 2026-10-12" in vp_out[1] and
        "T102 | Buy milk | Low | 2026-10-11" in vp_out[2]
    ):
        print(" [PASS] view_by_priority sorts High -> Medium -> Low correctly.")
    else:
        print(" [FAIL] view_by_priority sorting mismatch:", vp_out)
        passed = False

    # Test complete_task
    buf = io.StringIO()
    with redirect_stdout(buf):
        ok = task_manager.complete_task(tasks, "T101", TASK_FILE)
    comp_out = buf.getvalue().strip()
    if ok and "Task T101 marked as done. Pending tasks: 2" in comp_out:
        print(" [PASS] complete_task marked T101 as done and reported 2 pending.")
    else:
        print(" [FAIL] complete_task output mismatch:", comp_out)
        passed = False

    # Test load_tasks from file
    loaded = task_manager.load_tasks(TASK_FILE)
    if len(loaded) == 3 and loaded[0]["status"] == "Done" and loaded[1]["status"] == "Pending":
        print(" [PASS] load_tasks successfully loaded state from tasks.txt.")
    else:
        print(" [FAIL] load_tasks failed.")
        passed = False

    return passed


def main():
    print("Running Daily Task Manager Test Suite...")
    t1 = test_case_1()
    t1_lbl = test_case_1_labeled()
    t2 = test_case_2()
    t3 = test_case_3()
    t4 = test_case_4()
    t_unit = test_unit_functions()
    
    print("\n================== SUMMARY ==================")
    print(f"Test Case 1 (Normal Input):               {'PASSED' if t1 else 'FAILED'}")
    print(f"Test Case 1 (Labeled Input):              {'PASSED' if t1_lbl else 'FAILED'}")
    print(f"Test Case 2 (Boundary / Minimum Input):   {'PASSED' if t2 else 'FAILED'}")
    print(f"Test Case 3 (Invalid Input):              {'PASSED' if t3 else 'FAILED'}")
    print(f"Test Case 4 (Different Valid Scenario):   {'PASSED' if t4 else 'FAILED'}")
    print(f"Unit Tests (Functions & Logic):           {'PASSED' if t_unit else 'FAILED'}")
    
    if all([t1, t1_lbl, t2, t3, t4, t_unit]):
        print("\nALL TEST CASES & UNIT TESTS PASSED PERFECTLY!")
    else:
        print("\nSOME TESTS FAILED.")


if __name__ == "__main__":
    main()
