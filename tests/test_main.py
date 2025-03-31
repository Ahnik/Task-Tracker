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
    '''Fixture to set up and tear down a temporary empty tasks.json file.'''
    # Create an empty temporary tasks.json file 
    tasks = []
    
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)
    
    yield   # Run the rests
    
    # Clean up: Remove the task files after tests
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
    
    # Clean up: Remove the task files after tests
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
    
    # Clean up: Remove the task files after tests
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
        
def run_cli_command(command):
    '''Helper function to run a CLI command'''
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout, result.returncode

def test_add_task_1(setup_1):
    '''Test for adding a new task when the JSON file is empty'''
    command = ['python3', MAIN_PATH, 'add', '"Buy groceries"']
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command ran successfully
    assert code == 0
    assert "Task added successfully (ID: 1)" in output
    
    # Verify the task is added to the JSON file
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
    
    assert len(tasks) == 1
    assert tasks[-1]['description'] == 'Buy groceries'
    
def test_add_task_2(setup_2):
    '''Test for adding a new task when the JSON file is not empty'''
    command = ['python3', MAIN_PATH, 'add', '"Buy groceries"']
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command ran successfully
    assert code == 0
    assert "Task added successfully (ID: 3)" in output
    
    # Verify the task is added to the JSON file
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    assert len(tasks) == 3
    assert tasks[-1]['description'] == 'Buy groceries'
    
def test_add_task_3(setup_3):
    '''Test for adding a new task when the JSON file is not empty and when there are already task IDs available'''
    command = ['python3', MAIN_PATH, 'add', '"Buy groceries"']
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command ran successfully
    assert code == 0
    assert "Task added successfully (ID: 2)" in output
    
    # Verify the task is added to the JSON file
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    assert len(tasks) == 5
    assert tasks[1]['description'] == 'Buy groceries'