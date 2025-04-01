'''Module containing the implementation of the Task class'''
from datetime import datetime
from pathlib import Path
import json
from heapq import heappop
from bisect import insort
from helper import print_task

class Task(object):
    '''Class for storing the contents of the tasks.json file and implementing the commands to be performed on the tasks'''
    # The constructor
    def __init__(self, filename = Path("../tasks.json").resolve()):
        '''An instance of this class will contain the data extracted from the tasks.json file'''
        self.filename = filename
        self.tasks = []             # Stores the task data
        self.available_ids = []     # Min-heap for storing deleted task IDs
        self.next_id = 1            # Next available task ID if no deleted IDs exist
        self.load_tasks()
    
    def load_tasks(self):
        '''Loads tasks from the JSON file'''
        try:
            with open(self.filename, 'r') as f:
                self.tasks = list(json.load(f))
                if self.tasks:
                    self.next_id = max(task['id'] for task in self.tasks) + 1
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
                
    def save_tasks(self):
        '''Save tasks to the JSON file'''
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)
        
    def add_task(self, description):
        '''Function to add a task'''
        if self.available_ids:
            task_id = heappop(self.available_ids)     # Get the smallest available IDs
        else:
            task_id = self.next_id
            self.next_id += 1
            
        # The task to be added
        task = {
            'id': int(task_id),
            'description': str(description),
            'status': 'todo',
            'createdAt': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'updatedAt': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # The task is inserted into self.tasks sorted with respect to the task ID
        insort(self.tasks, task, key=lambda d: d['id'])        
        
    def update_task(self, id, description):
        '''Function to update the description of a task'''
        if not self.tasks:
            return 1        # Return status code 1 to indicate that no task has been added
        for task in self.tasks:
            if task['id'] == id:
                task['description'] = str(description)
                task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return 0    # Return status code 0 to indicate success
        return -1           # Return status code -1 to indicate no task with that task ID could be found
        
    def delete_task(self, id):
        '''Function to delete a task'''
        if not self.tasks:
            return 1        # Return status code 1 to indicate that no task has been added
        for task in self.tasks:
            if task['id'] == id:
                self.tasks.remove(task)
                return 0    # Return status code 0 to indicate success
        return -1           # Return status code -1 to indicate no task with that task ID could be found
        
    def list_task(self):
        '''Funnction to list out all the tasks'''
        if not self.tasks:
            return 1        # Return status code 1 to indicate that no task has been added
        for task in self.tasks:
            print_task(task)
        return 0            # Return status code 0 to indicate success
        
    def list_todo(self):
        '''Function to list out all the tasks marked "todo"'''
        if not self.tasks:
            return 1        # Return status code 1 to indicate that no task has been added
        for task in self.tasks:
            if task['status'] == 'todo':
                print_task(task)
        return 0            # Return status code 0 to indicate success
        
    def list_in_progress(self):
        '''Function to list out all the tasks marked "in-progress"'''
        if not self.tasks:
            return 1        # Return status code 1 to indicate that no task has been added
        for task in self.tasks:
            if task['status'] == 'in-progress':
                print_task(task)
        return 0            # Return status code 0 to indicate success
        
    def list_done(self):
        '''Function to list out all the tasks marked "done"'''
        if not self.tasks:
            return 1        # Return status code 1 to indicate that no task has been added
        for task in self.tasks:
            if task['status'] == 'done':
                print_task(task)
        return 0            # Return status code 0 to indicate success
                
    def mark_in_progress(self, id):
        '''Function to mark the status of a certain task as "in-progress"'''
        for task in self.tasks:
            if task['id'] == id:
                # Return status code -2 if the status is already set to "in-progress"
                if task['status'] == 'in-progress':
                    return -2
                # Return status code -3 if the status is set to "done"
                elif task['status'] == 'done':
                    return -3
                task['status'] = 'in-progress'
                task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return 0    # Return status code 0 to indicate success
        return -1       # Return status code -1 if no task with that ID exists
                
        
    def mark_done(self, id):
        '''Function to mark the status of a certain task as "done"'''
        for task in self.tasks:
            if task['id'] == id:
                # Return status code -2 if the status is already set to "in-progress"
                if task['status'] == 'done':
                    return -2
                task['status'] = 'done'
                task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return 0
        return -1       # Return status code -1 if no task with that ID exists