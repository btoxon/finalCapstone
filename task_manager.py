# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"


# Define function to create tasks list from tasks.txt
def load_tasks():
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)
    return task_list

# Define function to create username-password dictionary from user.txt
def load_users():
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    return username_password

# Define function to handle user registration
def reg_user(username_password):
    new_username = input("New Username: ")
    if new_username in username_password.keys():
        print("Username already exists. Try a different username.")
        return

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = [f"{k};{username_password[k]}" for k in username_password]
            out_file.write("\n".join(user_data))
    else:
        print("Passwords do not match")

# Define function to add a new task
def add_task(task_list, username_password):
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = [
            ";".join([
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]) for t in task_list
        ]
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# Define function to view all tasks
def view_all(task_list):
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# Define function to view tasks assigned to the current user
def view_mine(task_list, curr_user):
    task_num = 1
    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"Task {task_num}:\n"
            disp_str += f"Title: \t {t['title']}\n"
            disp_str += f"Assigned on: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Description: \t {t['description']}\n"
            disp_str += f"Completed: \t {'Yes' if t['completed'] else 'No'}\n"
            print(disp_str)
            task_num += 1

    print(f"{task_num}. Return to main menu")

# Define function to generate reports
def generate_reports(task_list, username_password):
    num_users = len(username_password)
    num_tasks = len(task_list)
    num_completed_tasks = sum(1 for t in task_list if t['completed'])
    num_incomplete_tasks = num_tasks - num_completed_tasks
    num_overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'] < date.today())

    # Task overview
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"Total tasks: {num_tasks}\n")
        task_overview_file.write(f"Completed tasks: {num_completed_tasks}\n")
        task_overview_file.write(f"Incomplete tasks: {num_incomplete_tasks}\n")
        task_overview_file.write(f"Overdue tasks: {num_overdue_tasks}\n")
        task_overview_file.write(f"Percentage of incomplete tasks: {(num_incomplete_tasks / num_tasks) * 100:.2f}%\n")
        task_overview_file.write(f"Percentage of overdue tasks: {(num_overdue_tasks / num_tasks) * 100:.2f}%\n")

    # User overview
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"Total users: {num_users}\n")
        user_overview_file.write(f"Total tasks: {num_tasks}\n")

        for user, password in username_password.items():
            user_tasks = [t for t in task_list if t['username'] == user]
            num_user_tasks = len(user_tasks)
            num_user_completed_tasks = sum(1 for t in user_tasks if t['completed'])
            num_user_incomplete_tasks = num_user_tasks - num_user_completed_tasks
            num_user_overdue_tasks = sum(1 for t in user_tasks if not t['completed'] and t['due_date'] < date.today())

            user_overview_file.write(f"\n{user}:\n")
            user_overview_file.write(f"  - Total tasks assigned: {num_user_tasks}\n")
            user_overview_file.write(f"  - Percentage of total tasks: {(num_user_tasks / num_tasks) * 100:.2f}%\n")
            user_overview_file.write(f"  - Percentage of completed tasks: {(num_user_completed_tasks / num_user_tasks) * 100:.2f}%\n")
            user_overview_file.write(f"  - Percentage of incomplete tasks: {(num_user_incomplete_tasks / num_user_tasks) * 100:.2f}%\n")
            user_overview_file.write(f"  - Percentage of overdue tasks: {(num_user_overdue_tasks / num_user_tasks) * 100:.2f}%\n")

#====Login Section====
#This code reads usernames and password from the user.txt file to allow a user to login.

task_list = load_tasks()
username_password = load_users()

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

while True:
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user(username_password)

    elif menu == 'a':
        add_task(task_list, username_password)

    elif menu == 'va':
        view_all(task_list)

    elif menu == 'vm':
        view_mine(task_list, curr_user)

    elif menu == 'gr' and curr_user == 'admin':
        generate_reports(task_list, username_password)
        print("Reports generated successfully.")

    elif menu == 'ds' and curr_user == 'admin':
        num_users = len(username_password)
        num_tasks = len(task_list)
        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice. Please try again")


























