#! usr/bin/env python3
import task
import sys

def main():
    '''The main function'''
    if len(sys.argv) < 2:
        # If no command is executed
        print("Usage: task-cli <command> <arguments>")
        return 2
    tasks = task.Task()     # An instance of the Task object is initialized
    
    if sys.argv[1] == 'add':
        '''If the command entered is "add"'''
        # If the command entered is invalid
        if len(sys.argv) != 3:
            print("Usage: task-cli add <description>")
            return 2
        # The task is added
        task_id = tasks.add_task(sys.argv[2])
        print("Task added successfully (ID: %d)"%(int(task_id)))
        
    elif sys.argv[1] == 'update':
        '''If the command entered is "update"'''
        # If the command entered is invalid
        if len(sys.argv) != 4:
            print("Usage: task-cli update <id> <description>")
            return 2
        # We attempt to update the task
        try:
            status = tasks.update_task(int(sys.argv[2]), sys.argv[3])
        except TypeError:
            print("Usage: task-cli update <int id> <str description>")
            return 2
        
        if status == 1:
            print("No tasks have been added yet")
        elif status == -1:
            print("Task ID %d does not exist"%(int(sys.argv[2])))
        elif status == 0:
            print("Task ID %d successfully updated"%(int(sys.argv[2])))
        
    elif sys.argv[1] == 'delete':
        '''If the command entered is "delete"'''
        # If the command entered is invalid
        if len(sys.argv) != 3:
            print("Usage: task-cli delete <id>")
            return 2
        # We attempt to delete the task
        try:
            status = tasks.delete_task(int(sys.argv[2]))
        except TypeError:
            print("Usage: task-cli delete <int id>")
            return 2
        
        if status == 1:
            print("No tasks have been added yet")
        elif status == -1:
            print("Task ID %d does not exist"%(int(sys.argv[2])))
        elif status == 0:
            print("Task ID %d successfully deleted"%(int(sys.argv[2])))

    tasks.save_tasks()  # The tasks are saved
    return 0            # Return status code for success
            
if __name__ == '__main__':
    main()