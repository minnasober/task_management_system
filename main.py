# main.py
from project_manager import project_manager_module
from team_lead import team_lead_module
from developer import developer_module
import msvcrt   # For Windows password masking
import sys
from db_utils import init_db
import psycopg2  # Changed from mysql.connector
from db_utils import get_connection

# Initialize database once at program start
try:
    init_db()
    print(" Database initialized successfully")
except Exception as e:
    print(f" Database initialization error: {e}")
    sys.exit(1)

# ------------------- USER ACCOUNTS -------------------
PROJECT_MANAGER_USERNAME = "admin"
PROJECT_MANAGER_PASSWORD = "admin123"

TEAM_LEAD_USERNAME = "teamlead"
TEAM_LEAD_PASSWORD = "lead123"

DEVELOPER_USERNAME = "developer"
DEVELOPER_PASSWORD = "dev123"


# ------------------- PASSWORD INPUT -------------------
def get_hidden_password(prompt="Password: "):
    """Get password input while showing asterisks"""
    print(prompt, end='', flush=True)
    password = ""
    while True:
        char = msvcrt.getwch()  # Read single character without showing it
        if char == '\r' or char == '\n':  # Enter key
            print()
            break
        elif char == '\b':  # Backspace
            if len(password) > 0:
                password = password[:-1]
                sys.stdout.write("\b \b")
                sys.stdout.flush()
        else:
            password += char
            sys.stdout.write("*")
            sys.stdout.flush()
    return password

# ------------------- SHOW ALL DEVELOPERS -------------------
def show_all_developers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, department, team_lead, qualification, 
               skills, experience, email, phone, join_date 
        FROM developers
    """)
    rows = cursor.fetchall()
    if not rows:
        print("\nNo developers found in the database.")
    else:
        print("\nAll Developers:")
        print("-" * 100)
        for row in rows:
            print(f"ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Department: {row[2] if row[2] else 'Not assigned'}")
            print(f"Team Lead: {row[3]}")
            print(f"Qualification: {row[4]}")
            print(f"Skills: {row[5]}")
            print(f"Experience: {row[6]} years")
            print(f"Email: {row[7]}")
            print(f"Phone: {row[8] if row[8] else 'Not provided'}")
            print(f"Join Date: {row[9]}")
            print("-" * 100)
    cursor.close()
    conn.close()

# ------------------- SHOW ALL TEAM LEADS -------------------
def show_all_teamleads():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, department, contact_no FROM team_leads")
    rows = cursor.fetchall()
    print("\nAll Team Leads:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Department: {row[2]}, Contact: {row[3]}")
    cursor.close()
    conn.close()

# ------------------- MAIN LOGIN FUNCTION -------------------
def main():
    while True:
        print("\n" + "=" * 40)
        print(" " * 10 + "TASK MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. Project Manager Login")
        print("2. Team Lead Login")
        print("3. Developer Login")
        print("4. Exit")

        choice = input("\nChoose an option (1-4): ")

        if choice == "1":
            username = input("Enter Project Manager username: ")
            password = get_hidden_password("Enter Project Manager password: ")
            if username == PROJECT_MANAGER_USERNAME and password == PROJECT_MANAGER_PASSWORD:
                print(" Project Manager login successful")
                project_manager_module()
            else:
                print(" Invalid Project Manager credentials")

        elif choice == "2":
            username = input("Enter Team Lead username: ")
            password = get_hidden_password("Enter Team Lead password: ")
            if username == TEAM_LEAD_USERNAME and password == TEAM_LEAD_PASSWORD:
                print(" Team Lead login successful")
                team_lead_module()
            else:
                print(" Invalid Team Lead credentials")

        elif choice == "3":
            username = input("Enter Developer username: ")
            password = get_hidden_password("Enter Developer password: ")
            if username == DEVELOPER_USERNAME and password == DEVELOPER_PASSWORD:
                print(" Developer login successful")
                developer_module()
            else:
                print(" Invalid Developer credentials")

        elif choice == "4":
            print(" Exiting... Goodbye!")
            break

        else:
            print(" Invalid choice. Try again.")


if __name__ == "__main__":
    main()      # run the main program
    show_all_developers()
    show_all_teamleads()
