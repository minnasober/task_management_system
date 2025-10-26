# project_manager.py
from datetime import datetime
from tabulate import tabulate
from db_utils import get_connection, init_db
from psycopg2 import Error  # Changed from mysql.connector

# ------------------- TASK FUNCTIONS -------------------
def add_task(title, team_lead, start_date, end_date, priority):
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        duration = (end - start).days + 1

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (title, team_lead, assigned_to, start_date, end_date, duration, priority)
            VALUES (%s, %s, NULL, %s, %s, %s, %s)
        """, (title, team_lead, start_date, end_date, duration, priority))
        conn.commit()
        cursor.close()
        conn.close()
        print(f" Task added: {title}")
    except ValueError:
        print(" Invalid date format. Use YYYY-MM-DD")


def list_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, team_lead, start_date, end_date, duration, priority, status
        FROM tasks
    """)
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()

    if not tasks:
        print("No tasks yet.")
        return

    formatted_tasks = []
    for task in tasks:
        task_id, title, team_lead, start_date, end_date, duration, priority, status = task
        formatted_tasks.append([
            task_id,
            title[:20],
            team_lead[:15],
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d'),
            f"{duration} days",
            priority,
            status
        ])

    headers = ["ID", "Title", "Team Lead", "Start Date", "End Date", "Duration", "Priority", "Status"]
    print("\n" + tabulate(formatted_tasks, headers=headers, tablefmt="grid"))


def update_status(index, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks ORDER BY id")
    task_ids = [row[0] for row in cursor.fetchall()]

    if 0 <= index < len(task_ids):
        task_id = task_ids[index]
        cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (new_status, task_id))
        conn.commit()
        print(f" Updated task {index + 1} status to {new_status}")
    else:
        print(" Invalid task number.")

    cursor.close()
    conn.close()


def delete_task(index):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM tasks ORDER BY id")
    tasks = cursor.fetchall()

    if 0 <= index < len(tasks):
        task_id, title = tasks[index]
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        print(f" Deleted task: {title}")
    else:
        print(" Invalid task number.")

    cursor.close()
    conn.close()


# ------------------- DEVELOPER FUNCTIONS -------------------
def add_developer():
    name = input("Enter developer name: ")
    department = input("Enter developer's department: ")
    team_lead = input("Enter developer's team lead name: ")
    qualification = input("Enter qualification: ")
    skills = input("Enter skills (comma separated): ")
    experience = int(input("Enter years of experience: "))
    email = input("Enter email address: ")
    phone = input("Enter phone number: ")

    while True:
        join_date = input("Enter join date (YYYY-MM-DD): ")
        try:
            datetime.strptime(join_date, '%Y-%m-%d')
            break
        except ValueError:
            print(" Invalid date format. Use YYYY-MM-DD")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO developers (name, department, team_lead, qualification, skills, 
                              experience, email, phone, join_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (name, department, team_lead, qualification, skills, 
          experience, email, phone, join_date))
    conn.commit()
    cursor.close()
    conn.close()
    print(f" Developer added: {name}")


def list_developers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, department, team_lead, qualification, 
               skills, experience, email, phone, join_date 
        FROM developers
    """)
    devs = cursor.fetchall()
    cursor.close()
    conn.close()

    if not devs:
        print("No developers added yet.")
        return

    formatted = []
    for dev in devs:
        dev_id, name, dept, lead, qual, skills, exp, email, phone, join_date = dev
        formatted.append([
            dev_id, name, dept, lead, qual,
            skills, f"{exp} years", email,
            phone, join_date.strftime('%Y-%m-%d')
        ])

    headers = ["ID", "Name", "Department", "Team Lead", "Qualification",
              "Skills", "Experience", "Email", "Phone", "Join Date"]
    print("\n Developers List:")
    print(tabulate(formatted, headers=headers, tablefmt="grid"))


# ------------------- TEAMLEAD FUNCTIONS -------------------
def add_teamlead():
    name = input("Enter team lead name: ")
    department = input("Enter department: ")
    team_members = input("Enter team members/developers (comma separated): ")
    contact_no = input("Enter contact no: ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO team_leads (name, department, team_members, contact_no)
        VALUES (%s, %s, %s, %s)
    """, (name, department, team_members, contact_no))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"👨 Team Lead added: {name}")


def list_teamleads():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, department, team_members, contact_no FROM team_leads")
    leads = cursor.fetchall()
    cursor.close()
    conn.close()

    if not leads:
        print("No team leads added yet.")
        return

    formatted = []
    for lead in leads:
        lead_id, name, dept, members, contact = lead
        formatted.append([lead_id, name, dept, members, contact])

    headers = ["ID", "Name", "Department", "Team Members", "Contact"]
    print("\n👨‍💼 Team Leads List:")
    print(tabulate(formatted, headers=headers, tablefmt="grid"))


# ------------------- MAIN MODULE -------------------
def project_manager_module():
    try:
        while True:
            print("\n" + "=" * 55)
            print(" " * 15 + "PROJECT MANAGER MODULE")
            print("=" * 55)
            print("1. Add New Task")
            print("2. Check Project Status")
            print("3. Update Status")
            print("4. Delete Task")
            print("5. Add Developer")
            print("6. List Developers")
            print("7. Add Team Lead")
            print("8. List Team Leads")
            print("9. Back to Main Menu")

            choice = input("\nChoose an option (1-9): ")

            if choice == "1":
                title = input("Enter task title: ")
                team_lead = input("Enter team lead name: ")

                while True:
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    try:
                        start = datetime.strptime(start_date, '%Y-%m-%d').date()
                        if start < datetime.now().date():
                            print(" Error: Start date cannot be in the past")
                            continue
                        break
                    except ValueError:
                        print(" Invalid date format. Use YYYY-MM-DD")

                while True:
                    end_date = input("Enter end date (YYYY-MM-DD): ")
                    try:
                        end = datetime.strptime(end_date, '%Y-%m-%d').date()
                        if end < start:
                            print(" Error: End date cannot be before start date")
                            continue
                        break
                    except ValueError:
                        print(" Invalid date format. Use YYYY-MM-DD")

                print("Priority levels: High, Medium, Low")
                priority = input("Enter priority: ")
                add_task(title, team_lead, start_date, end_date, priority)

            elif choice == "2":
                list_tasks()
                input("\nPress Enter to continue...")

            elif choice == "3":
                try:
                    list_tasks()
                    index = int(input("\nTask number to update: ")) - 1
                    print("Status options: Not Started, In Progress, Completed, On Hold")
                    new_status = input("Enter new status: ")
                    update_status(index, new_status)
                except ValueError:
                    print(" Please enter a valid number.")

            elif choice == "4":
                try:
                    list_tasks()
                    index = int(input("\nTask number to delete: ")) - 1
                    delete_task(index)
                except ValueError:
                    print(" Please enter a valid number.")

            elif choice == "5":
                add_developer()

            elif choice == "6":
                list_developers()
                input("\nPress Enter to continue...")

            elif choice == "7":
                add_teamlead()

            elif choice == "8":
                list_teamleads()
                input("\nPress Enter to continue...")

            elif choice == "9":
                break

            else:
                print(" Invalid choice. Try again.")
    except Error as e:
        print(f"Error: {e}")
