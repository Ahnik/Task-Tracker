'''Module storing all the helper functions necessary in the program'''

def print_task(task):
    '''Function to print the contents of a task on the stdout'''
    print("id: ", end='')
    print(task['id'])
    print("description: ", end='')
    print(task['description'])
    print("status: ", end='')
    print(task['status'])
    print("createdAt: ", end='')
    print(task['createdAt'])
    print("updatedAt: ", end='')
    print(task['updatedAt'])
    print('*'*20)