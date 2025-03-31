import pytest
import subprocess
import os
from pathlib import Path
import json
from datetime import datetime

# Path to the tasks.json file
TASKS_FILE = Path("../tasks.json").resolve()

# Path to the main file
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

# The following functions are tests for the 'delete' command
def test_delete_task_1(setup_1):
    '''Test for trying to delete a task when there are no tasks added'''
    command = ['python3', MAIN_PATH, 'delete', 1]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "No tasks have been added yet\n" in output
    
def test_delete_task_2(setup_2):
    '''Test for trying to delete a non-existing task from a non-empty tasks file'''
    command = ['python3', MAIN_PATH, 'delete', 5]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "Task ID 5 does not exist\n" in output
    
def test_delete_task_3(setup_2):
    '''Test for trying to delete an existing task'''
    command = ['python3', MAIN_PATH, 'delete', 4]
    
    # Run the CLI command
    output, code = run_cli_command(command)

    # Verify the command run was unsuccessful
    assert code == 0
    assert "Task ID 4 successfully deleted\n" in output
    
    # Verify the task is deleted in the JSON file
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    assert len(tasks) == 3
    assert not any(item['id'] == 4 for item in tasks)