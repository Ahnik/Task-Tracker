import pytest
import subprocess
import os
import sys
from pathlib import Path
import json
from datetime import datetime

# Add the app directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

# Import functions from main.py
from main import add_task, update_task, delete_task, mark_in_progress, mark_done, list_tasks

# Path to the tasks.json file
TASKS_FILE = Path("../tasks.json").resolve()

# Path to your task tracker script
MAIN_PATH = Path("../app/main.py").resolve()

@pytest.fixture(scope="module")
def setup_1():
    '''Fixture to run tests with no tasks.json file and tear down any tasks.json file created afterwards'''
    # If a tasks.json file exists, remove it
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
        
    yield   # Run the rests
    
    # Clean up: Remove the task file after tests
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
        
@pytest.fixture(scope="module")
def setup_2():
    '''Fixture to set up and tear down a temporary non-empty tasks.json file.'''
    # Create a non-empty temporary tasks.json file
    tasks = [
        {
            'id': 1, 
            'description': 'Finish project report', 
            'status': 'todo', 
            'createdAt': datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
            'updatedAt': datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        }, 
        {
            'id': 2,
            'description': 'Write unit tests',
            'status': 'in-prograss',
            'createdAt': datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
            'updatedAt': datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        }
    ]
    
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)
        
    yield   # Run the tests
    
    # Clean up: Remove the task file after tests
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
        
@pytest.fixture(scope="module")
def setup_3():
    '''Fixture to set up and tear down a temporary non-empty tasks.json file with missing IDs.'''
    # Create temporary tasks.json file
    tasks = [
        {
            'id': 1, 
            'description': 'Finish project report', 
            'status': 'todo', 
            'createdAt': datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
            'updatedAt': datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        }, 
        {
            'id': 3,
            'description': 'Write unit tests',
            'status': 'in-prograss',
            'createdAt': datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
            'updatedAt': datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        },
        {
            'id': 4,
            'description': 'Finish college assignment',
            'status': 'done',
            'createdAt': datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
            'updatedAt': datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        },
        {
            'id': 6,
            'description': 'Go to the gym',
            'status': 'in-progress',
            'createdAt': datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
            'updatedAt': datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        }
    ]
    
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)
        
    yield   # Run the tests
    
    # Clean up: Remove the task file after tests
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
        
def run_cli_command(command):
    '''Helper function to run a CLI command'''
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout, result.returncode

# The following functions are tests for the 'add' command
def test_add_task_1(setup_1):
    '''Test for adding a new task when there is no JSON file'''
    command = ['python3', MAIN_PATH, 'add', '"Buy groceries"']
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Time at which the task is created
    now = datetime.now().strftime()
    
    # Verify the command ran successfully
    assert code == 0
    assert "Task added successfully (ID: 1)\n" in output
    
    # Verify whether tasks.json file is created
    assert os.path.exists(TASKS_FILE)
    
    # Verify the task is added to the JSON file
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
    
    assert len(tasks) == 1
    assert tasks[0]['description'] == 'Buy groceries'
    assert tasks[0]['createdAt'] == now
    assert tasks[0]['updatedAt'] == now
    
def test_add_task_2(setup_2):
    '''Test for adding a new task when the JSON file is not empty'''
    command = ['python3', MAIN_PATH, 'add', '"Buy groceries"']
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Time at which the task is created
    now = datetime.now().strftime()
    
    # Verify the command ran successfully
    assert code == 0
    assert "Task added successfully (ID: 3)\n" in output
    
    # Verify the task is added to the JSON file
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    assert len(tasks) == 3
    assert tasks[-1]['description'] == 'Buy groceries'
    assert tasks[-1]['createdAt'] == now
    assert tasks[-1]['updatedAt'] == now
    
def test_add_task_3(setup_3):
    '''Test for adding a new task when the JSON file is not empty and when there are already task IDs available'''
    command = ['python3', MAIN_PATH, 'add', '"Buy groceries"']
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Time at which the task is created
    now = datetime.now().strftime()
    
    # Verify the command ran successfully
    assert code == 0
    assert "Task added successfully (ID: 2)\n" in output
    
    # Verify the task is added to the JSON file
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    assert len(tasks) == 5
    assert tasks[1]['id'] == 2
    assert tasks[1]['description'] == 'Buy groceries'
    assert tasks[1]['createdAt'] == now
    assert tasks[1]['updatedAt'] == now

# The following functions are tests for the 'update' command
def test_update_task_1(setup_1):
    '''Test for updating a task when there are no tasks added'''
    command = ['python3', MAIN_PATH, 'update', 1, 'Buy groceries and cook dinner']
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "No tasks have been added yet\n" in output
    
def test_update_task_2(setup_3):
    '''Test for updating a non-existing tasks in a non-empty tasks file'''
    command = ['python3', MAIN_PATH, 'update', 5, 'Buy groceries and cook dinner']
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "Task ID 5 does not exist\n" in output
    
def test_update_task_3(setup_3):
    '''Test for successfully updating a task in a non-empty tasks file'''
    command = ['python3', MAIN_PATH, 'update', 4, 'Buy groceries and cook dinner']
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # The time at which the task is updated
    now = datetime.now().strftime()
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "Task ID 4 successfully updated\n" in output
    
    # Verify the task is updated in the JSON file
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    assert len(tasks) == 4
    assert tasks[2]['id'] == 4
    assert tasks[2]['description'] == 'Buy groceries and cook dinner'
    assert tasks[2]['updatedAt'] == now
    
# The following functions are tests for the 'delete' command
def test_delete_task_1(setup_1):
    '''Test for trying to delete a task when there are no tasks added'''
    command = ['python3', MAIN_PATH, 'delete', 1]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "No tasks have been added yet\n" in output
    
def test_delete_task_2(setup_3):
    '''Test for trying to delete a non-existing task from a non-empty tasks file'''
    command = ['python3', MAIN_PATH, 'delete', 5]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "Task ID 5 does not exist\n" in output
    
def test_delete_task_3(setup_3):
    '''Test for trying to delete an existing task'''
    command = ['python3', MAIN_PATH, 'delete', 4]
    
    # Run the CLI command
    output, code = run_cli_command(command)

    # Verify the command run was unsuccessful
    assert code != 0
    assert "Task ID 4 successfully deleted\n" in output
    
    # Verify the task is deleted in the JSON file
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    assert len(tasks) == 3
    assert not any(item['id'] == 4 for item in tasks)
    
# The following functions are tests for the 'mark-in-progress' and 'mark-done' commands
def test_mark_1(setup_1):
    '''Test for trying to mark a task when there are no tasks added'''
    # Testing for mark-in-progress
    command = ['python3', MAIN_PATH, 'mark-in-progress', 1]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "No tasks have been added yet\n" in output
    
    # Testing for mark-done
    command = ['python3', MAIN_PATH, 'mark-done', 1]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "No tasks have been added yet\n" in output
    
def test_mark_2(setup_3):
    '''Test for trying to mark a non-existent task from a non-empty tasks.json'''
    # Testing for mark-in-progress
    command = ['python3', MAIN_PATH, 'mark-in-progress', 5]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "Task ID 5 does not exist\n" in output
    
    # Testing for mark-done
    command = ['python3', MAIN_PATH, 'mark-done', 5]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "Task ID 5 does not exist\n" in output
    
def test_mark_3(setup_3):
    '''Test for trying to mark an existing task'''
    # Testing for mark-in-progress
    command = ['python3', MAIN_PATH, 'mark-in-progress', 4]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # The time when the task was updated
    now = datetime.now().strftime()
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "Task ID 4 marked 'in-progress' successfully\n" in output
    
    # Verify the task was updated
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    assert len(tasks) == 4
    assert tasks[2]['id'] == 4
    assert tasks[2]['status'] == 'in-progress'
    assert tasks[2]['updatedAt'] == now
    
    # Testing for mark-done
    command = ['python3', MAIN_PATH, 'mark-done', 3]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # The time when the task was updated
    now = datetime.now().strftime()
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "Task ID 3 marked 'done' successfully\n" in output
    
    # Verify the task was updated
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    assert len(tasks) == 4
    assert tasks[1]['id'] == 3
    assert tasks[1]['status'] == 'done'
    assert tasks[1]['updatedAt'] == now