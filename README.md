<h1>Requirements</h1>
<p>
The task tracker application should run from the command line, accept user actions and inputs as arguments, and store the tasks in a 
JSON file. The user should be able to: <br>
1. Add, Update, and Delete tasks<br>
2. Mark a test as in progress or done<br>
3. List all tasks<br>
4. List all tasks that are done<br>
5. List all tasks that are not done<br>
6. List all tasks that are in progress<br>
</p>

<h1>Constraints</h1>
<p>
1. Use positional arguments in command line to accept user inputs.<br>
2. Use a JSON file to store the tasks in the current directory.<br>
3. The JSON file should be created if it does not exist.<br>
</p>

<h1>List of commands and their usage</h1>
<p>
# Adding a new task
task-cli add "Buy groceries"
# Output: Task added successfully (ID: 1)

# Updating and deleting tasks
task-cli update 1 "Buy groceries and cook dinner"
task-cli delete 1

# Marking a task as in progress or done
task-cli mark-in-progress 1
task-cli mark-done 1

# Listing all tasks
task-cli list

# Listing tasks by status
task-cli list done
task-cli list todo
task-cli list in-progress
</p>

<h1>Task Properties</h1>
<p>
Each task should have the following properties:<br>
1. id: A unique identifier for the task<br>
2. description: A short description of the task<br>
3. status: The status of the task(todo, in-progress, done)<br>
4. createdAt: The date and time when the task was created<br>
5. updatedAt: The date and time when the task was last updated<br>
Make sure to add these properties to the JSON file when adding a new task and update them when updating the task.
</p>

<h1>Guide</h1>
<a href="https://roadmap.sh/projects/task-tracker">https://roadmap.sh/projects/task-tracker</a>