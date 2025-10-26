# view_tables.py
import psycopg2
from tabulate import tabulate
import sys

def view_all_tables():
    print("\n" + "="*80)
    print("CONNECTING TO DATABASE...")
    print("="*80)
    
    try:
        # Try to connect
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="minna",
            password="sober@19",
            database="miniprojectdatabase"
        )
        print(" Connected to database successfully!\n")
        
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        if not tables:
            print("⚠️ No tables found in database!")
            return
        
        print(f" Found {len(tables)} table(s)\n")
        
        # Show each table
        for table_tuple in tables:
            table_name = table_tuple[0]
            
            print("\n" + "="*80)
            print(f"TABLE: {table_name.upper()}")
            print("="*80)
            
            # Get columns
            cursor.execute(f"""
                SELECT column_name, data_type, character_maximum_length, is_nullable
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            
            print("\nSTRUCTURE:")
            col_data = []
            for col in columns:
                col_data.append([
                    col[0],  # column name
                    col[1],  # data type
                    col[2] if col[2] else '-',  # max length
                    col[3]   # nullable
                ])
            print(tabulate(col_data, headers=["Column", "Type", "Max Length", "Nullable"], tablefmt="simple"))
            
            # Count rows
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            print(f"\n Total Rows: {row_count}")
            
            # Show data
            if row_count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                rows = cursor.fetchall()
                col_names = [desc[0] for desc in cursor.description]
                
                print(f"\n Sample Data (showing {min(5, row_count)} of {row_count} rows):")
                print(tabulate(rows, headers=col_names, tablefmt="simple"))
            else:
                print("\n No data in this table")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*80)
        print(" Inspection complete!")
        print("="*80 + "\n")
        
    except psycopg2.OperationalError as e:
        print(f"\n Connection Error: {e}")
        print("\nCheck:")
        print("  1. PostgreSQL service running?")
        print("  2. Username/password correct?")
        print("  3. Database exists?")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    view_all_tables()
    input("\nPress Enter to exit...")
