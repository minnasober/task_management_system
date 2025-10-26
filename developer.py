# developer.py
from tabulate import tabulate
from db_utils import get_connection
from psycopg2 import Error  # Changed from mysql.connector


def view_my_tasks(developer_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, team_lead, start_date, end_date, priority, status
        FROM tasks
        WHERE assigned_to = %s
        ORDER BY priority DESC, end_date ASC
    """, (developer_name,))
    tasks = cursor.fetchall()
    if not tasks:
        print(f"\n No tasks assigned to you.")
    else:
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
        print("\n Your Tasks:")
        print(tabulate(formatted_tasks, headers=headers, tablefmt="grid"))
    cursor.close()
    conn.close()
    input("\nPress Enter to continue...")


def update_project_started(developer_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get the tasks for this developer
        cursor.execute("""
            SELECT id, title 
            FROM tasks 
            WHERE assigned_to = %s
        """, (developer_name,))
        
        tasks = cursor.fetchall()
        if not tasks:
            print("\n No tasks assigned to you.")
            cursor.close()
            conn.close()
            return
        
        # Show available tasks
        print("\n Your Tasks:")
        for task_id, title in tasks:
            print(f"{task_id}. {title}")
        
        # Ask about project status
        started = input("\nHave you started working on this project? (yes/no): ").lower()
        
        if started not in ['yes', 'no']:
            print(" Please answer with 'yes' or 'no'")
            cursor.close()
            conn.close()
            return
                
        # Update all tasks for this developer
        new_status = "In Progress" if started == 'yes' else "Not Started"
        
        cursor.execute("""
            UPDATE tasks 
            SET status = %s 
            WHERE assigned_to = %s
        """, (new_status, developer_name))
        
        conn.commit()
        if started == 'yes':
            print("\n Great! All your tasks are marked as 'In Progress'")
        else:
            print("\n Noted. All your tasks are marked as 'Not Started'")
        
        cursor.close()
        conn.close()
            
    except Error as e:
        print(f"Error: {e}")
    input("\nPress Enter to continue...")


def view_task_details(developer_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # PostgreSQL uses TO_CHAR for date formatting instead of DATE_FORMAT
        cursor.execute("""
            SELECT title, team_lead, assigned_to, TO_CHAR(start_date, 'YYYY-MM-DD') as start_date,
                   TO_CHAR(end_date, 'YYYY-MM-DD') as end_date, duration, priority, status, done
            FROM tasks
            WHERE assigned_to = %s
        """, (developer_name,))
        
        tasks = cursor.fetchall()
        if not tasks:
            print("\n⚠️ No tasks assigned to you.")
        else:
            for task in tasks:
                print("\n📌 Task Details")
                print("=" * 50)
                print(f"Title: {task[0]}")
                print(f"Team Lead: {task[1]}")
                print(f"Assigned To: {task[2]}")
                print(f"Start Date: {task[3]}")
                print(f"End Date: {task[4]}")
                print(f"Duration: {task[5]} days")
                print(f"Priority: {task[6]}")
                print(f"Status: {task[7]}")
                print(f"Completed: {'Yes' if task[8] else 'No'}")
                print("=" * 50)
        
        cursor.close()
        conn.close()
        input("\nPress Enter to continue...")
    except Error as e:
        print(f"Error: {e}")


def developer_module():
    try:
        developer_name = input("\nEnter your name (as assigned in tasks): ")
        while True:
            print("\n" + "=" * 50)
            print(" " * 15 + "DEVELOPER MODULE")
            print("=" * 50)
            print("1. View My Tasks")
            print("2. Project Started/Not Started")
            print("3. View Task Details")
            print("4. Back to Main Menu")

            choice = input("\nChoose an option (1-4): ")
            if choice == "1":
                view_my_tasks(developer_name)
            elif choice == "2":
                update_project_started(developer_name)
            elif choice == "3":
                view_task_details(developer_name)
            elif choice == "4":
                break
            else:
                print("Invalid choice. Try again.")
    except Error as e:
        print(f"Error: {e}")
