import pytest
import subprocess
import os
import json
from datetime import datetime

# Path to the tasks.json file
TASKS_FILE = os.path.abspath("../tasks.json")

# Path to the main file
MAIN_PATH =  os.path.abspath("../app/main.py")

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
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
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
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Verify the command ran successfully
    assert code == 0
    assert "Task added successfully (ID: 3)\n" in output
    
    # Verify the task is added to the JSON file
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    assert len(tasks) == 3
    assert tasks[-1]['description'] == '"Buy groceries"'
    assert tasks[-1]['createdAt'] == now
    assert tasks[-1]['updatedAt'] == now
    
def test_add_task_3(setup_3):
    '''Test for adding a new task when the JSON file is not empty and when there are already task IDs available'''
    command = ['python3', MAIN_PATH, 'add', '"Buy groceries"']
    
    # Run the CLI command
    output, code = run_cli_command(command)
    
    # Time at which the task is created
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Verify the command ran successfully
    assert code == 0
    assert "Task added successfully (ID: 2)\n" in output
    
    # Verify the task is added to the JSON file
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
        
    assert len(tasks) == 5
    assert tasks[1]['id'] == 2
    assert tasks[1]['description'] == '"Buy groceries"'
    assert tasks[1]['createdAt'] == now
    assert tasks[1]['updatedAt'] == now