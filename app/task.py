'''Module containing the implementation of the Task class'''

class Task(object):
    '''Class for storing the contents of the tasks.json file and implementing the commands to be performed on the tasks'''
    # The constructor
    def __init__(self, data):
        '''An instance of this class will contain the data extracted from the tasks.json file'''
        self.data = data
    
    def add_task(self, description):
        '''Function to add a task'''
        
    def update_task(self, id, description):
        '''Function to update the description of a task'''
        
    def delete_task(self, id):
        '''Function to delete a task'''
        
    def list_task(self):
        '''Funnction to list out all the tasks'''
        
    def list_todo(self):
        '''Function to list out all the tasks marked "todo"'''
        
    def list_in_progress(self):
        '''Function to list out all the tasks marked "in-progres"'''
        
    def list_done(self):
        '''Function to list out all the tasks marked "done"'''