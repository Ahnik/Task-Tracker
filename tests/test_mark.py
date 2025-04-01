import pytest
import subprocess
import os
import json
from datetime import datetime

# Path to the tasks.json file
TASKS_FILE = os.path.abspath("../tasks.json")

# Path to the main file
MAIN_PATH = os.path.abspath("../app/main.py")

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
    
def test_mark_2(setup_2):
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
    
def test_mark_3(setup_2):
    '''Test for trying to mark an existing task'''
    # Testing for mark-in-progress
    command = ['python3', MAIN_PATH, 'mark-in-progress', 1]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # The time when the task was updated
    now = datetime.now().strftime()
    
    # Verify the command run was unsuccessful
    assert code == 0
    assert "Task ID 1 marked 'in-progress' successfully\n" in output
    
    # Verify the task was updated
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    assert len(tasks) == 4
    assert tasks[0]['id'] == 1
    assert tasks[0]['status'] == 'in-progress'
    assert tasks[0]['updatedAt'] == now
    
    # Testing for mark-done
    command = ['python3', MAIN_PATH, 'mark-done', 3]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # The time when the task was updated
    now = datetime.now().strftime()
    
    # Verify the command run was unsuccessful
    assert code == 0
    assert "Task ID 3 marked 'done' successfully\n" in output
    
    # Verify the task was updated
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    assert len(tasks) == 4
    assert tasks[1]['id'] == 3
    assert tasks[1]['status'] == 'done'
    assert tasks[1]['updatedAt'] == now
    
def test_mark_4(setup_2):
    '''Test for trying to mark a task invalidly'''
    # Testing for mark-in-progress trying to mark a task 'in-progress' that is already 'in-progress'
    command = ['python3', MAIN_PATH, 'mark-in-progress', 3]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "Task ID 3 is already marked 'in-progress'\n" in output
    
    # Testing for mark- trying to mark a task 'done' when it is already 'done'
    command = ['python3', MAIN_PATH, 'mark-done', 4]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "Task ID 4 is already marked 'done'\n" in output
    
    # Testing for mark-in-progress trying to mark a task marked 'done' as 'in-progress'
    command = ['python3', MAIN_PATH, 'mark-in-progress', 4]
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Verify the command run was unsuccessful
    assert code != 0
    assert "Task ID 4 is marked 'done'. It cannot be marked 'in-progress'.\n" in output