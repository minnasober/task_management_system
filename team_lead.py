# team_lead.py
from tabulate import tabulate
from db_utils import get_connection
from project_manager import list_tasks   # reuse listing function
from psycopg2 import Error  # Changed from mysql.connector


def assign_task_to_developer():
    try:
        print("\nUnassigned Tasks:")
        conn = get_connection()
        cursor = conn.cursor()
        
        # Show only unassigned tasks
        cursor.execute("""
            SELECT id, title, team_lead, start_date, end_date, priority, status
            FROM tasks
            WHERE assigned_to IS NULL
            ORDER BY priority DESC, end_date ASC
        """)
        tasks = cursor.fetchall()
        
        if not tasks:
            print("\n No unassigned tasks available.")
            return
            
        formatted_tasks = []
        for task in tasks:
            task_id, title, team_lead, start_date, end_date, priority, status = task
            formatted_tasks.append([
                task_id,
                title,
                team_lead,
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d'),
                priority,
                status
            ])
        headers = ["ID", "Title", "Team Lead", "Start Date", "End Date", "Priority", "Status"]
        print("\n" + tabulate(formatted_tasks, headers=headers, tablefmt="grid"))
        
        task_id = input("\nEnter Task ID to assign: ")
        developer_name = input("Enter Developer Name: ")

        cursor.execute("""
            UPDATE tasks 
            SET assigned_to = %s 
            WHERE id = %s AND assigned_to IS NULL
        """, (developer_name, task_id))
        conn.commit()
        print(f"\n Task assigned to {developer_name} successfully!")
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error: {e}")


def view_developer_tasks():
    developer_name = input("\nEnter Developer Name to view tasks: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, start_date, end_date, priority, status
        FROM tasks
        WHERE team_lead = %s
    """, (developer_name,))
    tasks = cursor.fetchall()
    if not tasks:
        print(f"\nNo tasks assigned to {developer_name}")
    else:
        formatted_tasks = []
        for task in tasks:
            task_id, title, start_date, end_date, priority, status = task
            formatted_tasks.append([
                task_id,
                title,
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d'),
                priority,
                status
            ])
        headers = ["ID", "Title", "Start Date", "End Date", "Priority", "Status"]
        print(f"\n Tasks assigned to {developer_name}:")
        print(tabulate(formatted_tasks, headers=headers, tablefmt="grid"))
    cursor.close()
    conn.close()
    input("\nPress Enter to continue...")


def update_task_status_team_lead():
    try:
        list_tasks()
        task_id = input("\nEnter Task ID to update status: ")
        print("\nStatus options: Not Started, In Progress, Completed, On Hold")
        new_status = input("Enter new status: ")

        conn = get_connection()
        cursor = conn.cursor()
        done = True if new_status.lower() == "completed" else False

        cursor.execute("""
            UPDATE tasks 
            SET status = %s, done = %s 
            WHERE id = %s
        """, (new_status, done, task_id))
        conn.commit()
        print(f"\n Task status updated to {new_status}")
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error: {e}")


def view_teamlead_tasks():
    try:
        team_lead_name = input("\nEnter your name (Team Lead): ")
        conn = get_connection()
        cursor = conn.cursor()
        
        # First verify if the team lead exists
        cursor.execute("""
            SELECT name FROM team_leads
            WHERE name = %s
        """, (team_lead_name,))
        
        if not cursor.fetchone():
            print("\n Team Lead not found!")
            return
            
        cursor.execute("""
            SELECT id, title, start_date, end_date, duration, priority, status
            FROM tasks
            WHERE team_lead = %s
            ORDER BY priority DESC, end_date ASC
        """, (team_lead_name,))
        
        tasks = cursor.fetchall()
        if not tasks:
            print(f"\n No tasks found for Team Lead: {team_lead_name}")
        else:
            formatted_tasks = []
            for task in tasks:
                formatted_tasks.append([
                    task[0],  # id
                    task[1],  # title
                    task[2].strftime('%Y-%m-%d'),  # start_date
                    task[3].strftime('%Y-%m-%d'),  # end_date
                    f"{task[4]} days" if task[4] else "N/A",  # duration
                    task[5],  # priority
                    task[6]   # status
                ])
            
            print(f"\n Tasks for Team Lead: {team_lead_name}")
            print("=" * 100)
            headers = ["ID", "Title", "Start Date", "End Date", "Duration", "Priority", "Status"]
            print(tabulate(formatted_tasks, headers=headers, tablefmt="grid"))
        
        cursor.close()
        conn.close()
        input("\nPress Enter to continue...")
    except Error as e:
        print(f"Error: {e}")


def view_department_developers():
    try:
        print("\n View Developers Under Your Leadership")
        print("=" * 50)
        team_lead_name = input("Enter your name (Team Lead): ")
        
        # First verify the team lead and get their department
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT department
            FROM team_leads
            WHERE name = %s
        """, (team_lead_name,))
        result = cursor.fetchone()
        
        if not result:
            print("\n Team Lead not found!")
            return
            
        department = result[0]
        
        # Now get all developers in this department under this team lead
        cursor.execute("""
            SELECT name, qualification, skills, experience, email, phone, join_date
            FROM developers
            WHERE department = %s AND team_lead = %s
            ORDER BY name
        """, (department, team_lead_name))
        
        developers = cursor.fetchall()
        
        if not developers:
            print(f"\n No developers found in department: {department} under team lead: {team_lead_name}")
        else:
            print(f"\n Developers in {department} Department (Team Lead: {team_lead_name})")
            print("=" * 100)
            formatted_devs = []
            for dev in developers:
                formatted_devs.append([
                    dev[0],  # name
                    dev[1],  # qualification
                    dev[2],  # skills
                    f"{dev[3]} years",  # experience
                    dev[4],  # email
                    dev[5] if dev[5] else "N/A",  # phone
                    dev[6].strftime('%Y-%m-%d')  # join_date
                ])
            
            headers = ["Name", "Qualification", "Skills", "Experience", "Email", "Phone", "Join Date"]
            print(tabulate(formatted_devs, headers=headers, tablefmt="grid"))
            
        cursor.close()
        conn.close()
        input("\nPress Enter to continue...")
    except Error as e:
        print(f"Error: {e}")


def team_lead_module():
    try:
        while True:
            print("\n" + "=" * 50)
            print(" " * 15 + "TEAM LEAD MODULE")
            print("=" * 50)
            print("1. View Developers Under Your Leadership")
            print("2. View Your Tasks")
            print("3. Assign Task to Developer")
            print("4. Update Task Status")
            print("5. Back to Main Menu")

            choice = input("\nChoose an option (1-5): ")

            if choice == "1":
                view_department_developers()
            elif choice == "2":
                view_teamlead_tasks()
            elif choice == "3":
                assign_task_to_developer()
            elif choice == "4":
                update_task_status_team_lead()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Try again.")
    except Error as e:
        print(f"Error: {e}")
        input("\nPress Enter to continue...")
