'''
Programme that allows user to login and create users and add tasks.
Users are able to sign in and amend their tasks and/or mark tasks as completed.
'''
import os
from datetime import datetime, date

user_pw = {}
DATETIME_STRING_FORMAT = "%Y-%m-%d"
task_list = []
user_report = []
logged_in = False

# Read user file to store logins
file = open("user.txt","r")

for line in file:
	user, password  = line.strip().split(';')
	user_pw[user] = password
		
file.close()

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# Read tasks file
with open("tasks.txt", 'r') as task_file:
	task_data = task_file.read().split("\n")
	task_data = [t for t in task_data if t != ""]

# Read task details into dictionary and add to list	
for t_str in task_data:
	curr_t = {}

	# Split by semicolon and manually add each component
	task_components = t_str.split(";")
	curr_t['username'] = task_components[0]
	curr_t['title'] = task_components[1]
	curr_t['description'] = task_components[2]
	curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
	curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
	curr_t['completed'] = True if task_components[5] == "Yes" else False

	task_list.append(curr_t)

# Register new user	
def reg_user():	
	new_user = input("Please enter new username: ")
	new_pw = input("Please enter a password: ")
	# - Request input of password confirmation.
	confirm_password = input("Confirm Password: ")
						
	# - Check if the new password and confirmed password are the same.
	if new_pw == confirm_password:
		if new_user in user_pw.keys():
			print("Username already exists, please enter a different username")
		else:
			file = open("user.txt","a+")
			file.write(f"\n{new_user}:{new_pw}")
			print("New user aded!\n")
			user_pw[new_user] = new_pw

	# - Otherwise present a relevant message.
	else:
		print("Passwords do not match")


'''Allow a user to add a new task to task.txt file
Prompt a user for the following: 
     - A username of the person whom the task is assigned to,
     - A title of a task,
     - A description of the task and 
     - the due date of the task.'''
def add_task():
	#username, title, start date, due date completed status
	assigned_user = input("Username to assign task to: ")
	
	if assigned_user not in user_pw.keys():
		print("User does not exist. Please enter a valid username\n")
	else:
		title = input("Title of the task: ")
		description = input("Description of the task: ")
		startDate = date.today()
		print(f"Start date of the task (YYYY-MM-DD): {startDate}")
		while True:		# Continue to request for date in correct format
			try:
				dueDate = input("Due date of the task (YYYY-MM-DD): ")
				due_date_time = datetime.strptime(dueDate, DATETIME_STRING_FORMAT)
				break

			except ValueError:
				print("Invalid datetime format. Please use the format specified")

		completed = "No"

		updt_task = {
            "username": assigned_user,
            "title": title,
            "description": description,
            "due_date": dueDate,
            "assigned_date": startDate,
            "completed": completed
        }

		task_list.append(updt_task)		# Add new task to task_list to be accessed and updated in current session

		# Write new task to file
		file = open("tasks.txt","a+")
		file.write(f"\n{assigned_user};{title};{description};{startDate};{dueDate};{completed}")
		print("\nTask successfully added.\n")


'''Display all tasks to the console in format of Output 2 presented in the task pdf 
(i.e. includes spacing and labelling) '''
def view_all():

	for t in task_list:
		disp_str = f"Task: \t\t {t['title']}\n"
		disp_str += f"Assigned to: \t {t['username']}\n"
		disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
		disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
		disp_str += f"Task complete? \t {('No', 'Yes')[t['completed']]}\n"
		disp_str += f"Task Description: \n {t['description']}\n"

		print(disp_str)


'''Reads the task task_list and prints to the console in the format of Output 2 
presented in the task pdf (i.e. includes spacing and labelling)'''
def view_mine(user):
	
	for count, t in enumerate(task_list, start=1):
		if t['username'] == user:
			disp_str = f"Task Number: \t {count}\n"
			disp_str += f"Task: \t\t {t['title']}\n"
			disp_str += f"Assigned to: \t {t['username']}\n"
			disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
			disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
			disp_str += f"Task complete? \t {('No', 'Yes')[t['completed']]}\n"
			disp_str += f"Task Description: \n {t['description']}\n"

			print(disp_str)

	select_task = int(input('''If you would like to edit a task, please enter the task number.
	Otherwise please key -1 to return to main menu. \n'''))
	if select_task == -1:
		return
	
	select_task = select_task - 1		# -1 to adjust for index starting at 0
	if select_task > len(task_list) - 1:
		print(f"Task {select_task} does not exist.\n")
	else:
		edit = input(''' Please choose from the following options:
	m - mark the task as complete
	t - edit the task \n:''')
		if edit == 'm' and task_list[select_task]['completed']:
			print("Task has already been marked as completed.\n")
		elif edit == 'm':
			task_list[select_task]['completed'] = True
			print(f"Task {select_task} has been marked as completed\n")
		elif edit == 't' and task_list[select_task]['completed']:
			print("Completed tasks cannot be edited.\n")
		else:
			print(f'''You can edit the following details in Task {select_task}:
	Currently assigned to: {task_list[select_task]['username']},
	Current due date: {task_list[select_task]['due_date']}\n''')
			
			while True:	# Keep asking for a username if incorrect username is entered
				new_assign = input("Please enter the username if you want to re-assign the task. Otherwise leave blank.\n")
				if new_assign == "":
					break
				elif new_assign not in user_pw:
					print("Username does not exist, please try again.\n")
				else:
					task_list[select_task]['username'] = new_assign
					break

			while True: # Keep asking for a valid date format unless blank, assign when valid date is entered
				try:
					new_due_date = input("Please enter a new due date (YYYY-MM-DD) or leave blank to keep original due date.\n")
					if new_due_date == "":
						break
					else:
						nw_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
						task_list[select_task]['due_date'] = nw_date
						break

				except ValueError:
					print("Invalid datetime format. Please use the format specified")
				
		with open("tasks.txt", "w") as file:
			task_list_to_write = []
			for t in task_list:
				str_attrs = [
                	t['username'],
                	t['title'],
                	t['description'],
                	t['due_date'].strftime(DATETIME_STRING_FORMAT),
                	t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                	"Yes" if t['completed'] else "No"
            	]
				task_list_to_write.append(";".join(str_attrs))
			file.write("\n".join(task_list_to_write))
		
		print("Task successfully updated.")


'''Generate two files:
	Task overview - Summary of all tasks
	USer overview - Summary of tasks under each user
'''
def generate_reports():
	
	#---------------------------------------------
	#			TASK OVERVIEW FILE
	#---------------------------------------------
	todays_date = datetime.today()
	complted_tsk = 0
	overdue = 0
	overdue_incomplt = 0

	# For all tasks count those that meet the if statement criterias
	for t in task_list:
		if t['completed'] == True:
			complted_tsk += 1	

		if t['due_date'] < todays_date:
			overdue += 1

		if (t['completed'] == True) and (t['due_date'] < todays_date):
			overdue_incomplt += 1

	# Write all results in formatted report, if file does not exist, create file
	with open("task_overview.txt", 'w+') as tsk_overvw:
		tsk_overvw.write("\n=====================================================================")
		tsk_overvw.write("\n\t\t\t\tTask Overview Report\n")
		tsk_overvw.write("=====================================================================")
		tsk_overvw.write(f"\nDate report generated: \t\t{todays_date.strftime('%d %B %Y')}\n\n")
		tsk_overvw.write(f"Number of tasks created: \t\t\t\t\t{len(task_list)}\n")
		tsk_overvw.write(f"Number of tasks completed: \t\t\t\t\t{complted_tsk}\n")
		tsk_overvw.write(f"Number of tasks uncompleted: \t\t\t\t{str((len(task_list)-complted_tsk))}\n")
		tsk_overvw.write(f"Number of tasks uncompleted and overdue : \t{overdue_incomplt}\n")
		tsk_overvw.write(f"Percentage of tasks incomplete: \t\t\t{(len(task_list)-complted_tsk) / len(task_list):.0%}\n")
		tsk_overvw.write(f"Percentage of tasks overdue: \t\t\t\t{overdue / len(task_list):.0%}\n")

	#---------------------------------------------
	#			USER OVERVIEW FILE
	#---------------------------------------------
	# Loop through each user and go through task list that meet if statements
	for u in user_pw.keys():
		u_assigned = 0
		u_compltd = 0 
		u_overdue = 0

		for t in task_list:
			if t['username'] == u:
				u_assigned += 1
			
			if t['username'] == u and t['completed'] == True:
				u_compltd += 1
			
			if t['username'] == u and (t['completed'] != True) and (t['due_date'] < todays_date):
				u_overdue += 1
		
		# Store each results for each user in dictionary
		user_stats = {
		"username": u,
		"assigned": u_assigned,
		"completed": u_compltd,
		"overdue": u_overdue
 	}
		user_report.append(user_stats)

	# Write all results in formatted report, if file does not exist, create file
	with open("user_overview.txt", 'w+') as usr_overvw:
		usr_overvw.write("\n=====================================================================")
		usr_overvw.write("\n\t\t\t\tUser Overview Report\n")
		usr_overvw.write("=====================================================================")
		usr_overvw.write(f"\nDate report generated: \t\t{todays_date.strftime('%d %B %Y')}\n\n")
		usr_overvw.write(f"Number of users: \t\t\t\t{len(user_pw)}\n")
		usr_overvw.write(f"Number of tasks: \t\t\t\t{len(task_list)}\n")
		usr_overvw.write("\nUser Breakdown\n")
		usr_overvw.write("--------------------------------")
		for u in user_report:
			usr_overvw.write(f"\nUser: {u['username']}\n\n")
			usr_overvw.write(f"Percentage of assigned tasks assigned: \t\t\t\t\t{u['assigned']/ len(task_list):.0%}\n")
			usr_overvw.write(f"Percentage of assigned tasks completed: \t\t\t\t{u['completed'] / u['assigned']:.0%}\n")
			usr_overvw.write(f"Percentage of assigned tasks uncompleted: \t\t\t\t{ (u['assigned'] - u['completed'])/ u['assigned']:.0%}\n")
			usr_overvw.write(f"Percentage of assigned tasks overdue and uncomplete: \t{u['overdue'] / u['assigned']:.0%}\n")
			usr_overvw.write("---------------------------------------------------------------------\n")

	print("\nTask overview and User overiew reports have been generated.\n")


'''If the user is an admin they can display statistics about number of users
and tasks.'''
def view_stats():
	# Generate the latest version of reports to read and display on console
	generate_reports()

	# Read file with the UTF-8 encode and print without the \t format
	with open('task_overview.txt', 'r+', encoding='utf-8') as f:
		contents = f.read().replace("\t","")
		print(contents) 
	
	with open('user_overview.txt', 'r+', encoding='utf-8') as f:
		contents = f.read().replace("\t","")
		print(contents) 
	
	
# Log in page, will keep asking for correct log in details
while not logged_in:
	print("\nLOGIN\n")
	username = input("Enter username: ")
	pw = input("Enter password: ")

	if username not in user_pw.keys():
		print("Incorrect username. Please try again\n")
	elif user_pw[username] != pw:
		print("Incorrect password. Please try again\n")
	else:
		print(f"\nWelcom {username}!\n")
		logged_in = True

# Main menu
while logged_in:
	menu = input('''Please select one of the following Options below:

	r - Registering a user
	a - Adding a task
	va - View all tasks
	vm - View my task
	gr - Generate reports
	ds - Display statistics (admin only)
	e - Exit

Option selected : ''').lower()

	if menu == 'r':
		reg_user()
	elif menu == 'a':
		add_task()
	elif menu == 'va':
		view_all()
	elif menu == 'vm':
		view_mine(username)
	elif menu == 'ds' and username == 'admin':
		view_stats()
	elif menu == 'ds' and username != 'admin':
		print("You do not have the right credentials to use access this.\n")
	elif menu == 'gr':
		generate_reports()
	elif menu == 'e':
		print("Goodbye!!!")
		exit()
	else:
		print("Input not recognised. Please Try again\n")
