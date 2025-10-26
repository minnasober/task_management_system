# db_utils.py
import psycopg2
from psycopg2 import Error, sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database Configuration
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "minna"
DB_PASSWORD = "sober@19"
DB_NAME = "miniprojectdatabase"

def get_connection():
    """Create and return DB connection"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def init_db():
    """Initialize database and required tables"""
    conn = None
    try:
        # First try to connect to the database directly
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            print(f" Connected to existing database '{DB_NAME}'")
        except Error:
            print(f" Database '{DB_NAME}' doesn't exist. Creating it...")
            # Connect to default 'postgres' database
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database="postgres"
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Create database
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DB_NAME)
            ))
            print(f" Database '{DB_NAME}' created successfully")
            
            cursor.close()
            conn.close()
            
            # Reconnect to new database
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            
        # Create tables
        cursor = conn.cursor()
        
        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                team_lead VARCHAR(255) NOT NULL,
                assigned_to VARCHAR(255),
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                duration INTEGER,
                priority VARCHAR(50) NOT NULL,
                status VARCHAR(50) DEFAULT 'Not Started',
                done BOOLEAN DEFAULT FALSE
            )
        """)
        print("✅ Tasks table ready")
        
        # Developers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS developers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(100),
                team_lead VARCHAR(100) NOT NULL,
                qualification VARCHAR(255) NOT NULL,
                skills VARCHAR(255) NOT NULL,
                experience INTEGER NOT NULL,
                email VARCHAR(100) NOT NULL,
                phone VARCHAR(20),
                join_date DATE NOT NULL
            )
        """)
        print(" Developers table ready")
        
        # Team leads table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS team_leads (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                department VARCHAR(100),
                team_members TEXT,
                contact_no VARCHAR(15)
            )
        """)
        print(" Team leads table ready")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("\n Database and tables are ready.")
        
    except Error as e:
        print(f" Error: {e}")
        if conn:
            conn.close()
