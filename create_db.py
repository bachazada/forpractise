import sqlite3


def create_database():
    """
    Create and connect to the SQLite database.
    """
    connection = sqlite3.connect("airline_reservation.db")
    print("Database created and connected successfully.")
    return connection


def create_tables(connection):
    """
    Define and create the tables: users, seats, and reservations.
    """
    cursor = connection.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT 0
    );
    ''')

    print("Table 'users' created successfully.")

    # Create seats table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS seats (
        seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        seat_number TEXT NOT NULL,
        row_number INTEGER NOT NULL,
        seat_type TEXT NOT NULL CHECK(seat_type IN ('window', 'aisle', 'middle')),
        class TEXT NOT NULL CHECK(class IN ('economy', 'business', 'first')),
        is_reserved BOOLEAN NOT NULL DEFAULT 0
    );
    ''')

    print("Table 'seats' created successfully.")

    # Create reservations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        seat_id INTEGER NOT NULL,
        reservation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (seat_id) REFERENCES seats(seat_id)
    );
    ''')

    print("Table 'reservations' created successfully.")

    connection.commit()


def insert_initial_data(connection):
    """
    Insert initial data into the users and seats tables.
    """
    cursor = connection.cursor()

    # Insert initial users
    users = [
        ("Bacha", "bacha_user", "password123", 0),
        ("Faranak", "faranak_user", "password123", 0),
        ("Jonas", "jonas_admin", "adminpassword", 1),
        ("Paul", "paul_user", "password123", 0)
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO users (name, username, password, is_admin)
    VALUES (?, ?, ?, ?);
    ''', users)

    print("Initial users inserted successfully.")

    # Insert initial seats
    rows = 10
    columns = ["A", "B", "C", "D", "E", "F"]
    seat_data = []

    for row in range(1, rows + 1):
        for column in columns:
            seat_number = f"{row}{column}"
            seat_type = "window" if column in ["A", "F"] else "middle" if column in ["B", "E"] else "aisle"
            seat_class = "economy"  # Default to economy class
            seat_data.append((seat_number, row, seat_type, seat_class, 0))

    cursor.executemany('''
    INSERT OR IGNORE INTO seats (seat_number, row_number, seat_type, class, is_reserved)
    VALUES (?, ?, ?, ?, ?);
    ''', seat_data)

    print("Initial seats inserted successfully.")

    connection.commit()


def fetch_and_display_data(connection):
    """
    Fetch and display all data from the users and seats tables for verification.
    """
    cursor = connection.cursor()

    # Fetch and display users
    print("\nUsers Table:")
    for row in cursor.execute('SELECT * FROM users;'):
        print(row)

    # Fetch and display seats
    print("\nSeats Table:")
    for row in cursor.execute('SELECT * FROM seats LIMIT 20;'):
        print(row)


if __name__ == "__main__":
    # Step 1: Create and connect to the database
    conn = create_database()

    try:
        # Step 2: Create tables
        create_tables(conn)

        # Step 3: Insert initial data
        insert_initial_data(conn)

        # Step 4: Fetch and display data
        fetch_and_display_data(conn)

    finally:
        # Close the connection
        conn.close()
        print("\nDatabase connection closed.")
