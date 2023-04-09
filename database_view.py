import sqlite3

def main():
    # Connect to the database
    conn = sqlite3.connect('database/attendance.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Get the names of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [row[0] for row in cursor.fetchall()]

    # Display the available table names to the user
    print("Available tables:")
    for i, table_name in enumerate(table_names):
        print(f"{i + 1}: {table_name}")

    # Prompt the user to choose a table
    table_choice = int(input("Enter the number of the table you want to select: "))

    try:
        # Get the chosen table name
        chosen_table = table_names[table_choice - 1]
        # Execute a SELECT query on the chosen table
        cursor.execute(f"SELECT * FROM {chosen_table}")

        # Retrieve the column names and results as a list of tuples
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()

        # Print the column names and results
        print("\nTable: {}".format(chosen_table))
        for column in columns:
            print("{:<20}".format(column), end="")
        print("")
        for row in results:
            for value in row:
                print("{:<20}".format(value), end="")
            print("")
        
    except Exception as e:
        print(f'Error: {e}')
    
    # Close the cursor and connection
    cursor.close()
    conn.close()
