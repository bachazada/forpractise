"Allow users to reserve seats and update the database."

def reserve_seat(connection, user_id, seat_number):
    cursor = connection.cursor()

    # Get the seat ID based on seat number
    cursor.execute('SELECT seat_id, is_reserved FROM seats WHERE seat_number = ?;', (seat_number,))
    seat = cursor.fetchone()

    if seat is None:
        print(f"Seat {seat_number} does not exist.")
        return

    seat_id, is_reserved = seat

    if is_reserved:
        print(f"Seat {seat_number} is already reserved.")
        return

    # Reserve the seat
    cursor.execute('''
    INSERT INTO reservations (user_id, seat_id)
    VALUES (?, ?);
    ''', (user_id, seat_id))

    cursor.execute('''
    UPDATE seats
    SET is_reserved = 1
    WHERE seat_id = ?;
    ''', (seat_id,))

    connection.commit()
    print(f"Seat {seat_number} has been successfully reserved by user ID {user_id}.")

"cancel reservation and only admin can do this"

def cancel_reservation(connection, seat_number):
    cursor = connection.cursor()

    # Get the seat ID and reservation details
    cursor.execute('SELECT seat_id, is_reserved FROM seats WHERE seat_number = ?;', (seat_number,))
    seat = cursor.fetchone()

    if seat is None:
        print(f"Seat {seat_number} does not exist.")
        return

    seat_id, is_reserved = seat

    if not is_reserved:
        print(f"Seat {seat_number} is not currently reserved.")
        return

    # Cancel the reservation
    cursor.execute('''
    DELETE FROM reservations
    WHERE seat_id = ?;
    ''', (seat_id,))

    cursor.execute('''
    UPDATE seats
    SET is_reserved = 0
    WHERE seat_id = ?;
    ''', (seat_id,))

    connection.commit()
    print(f"Reservation for seat {seat_number} has been successfully canceled.")

'''Admin-Specific Queries
Generate reports like available seats, reserved seats, and user information'''

def generate_report(connection):
    cursor = connection.cursor()

    # Count available and reserved seats
    cursor.execute('SELECT COUNT(*) FROM seats WHERE is_reserved = 0;')
    available_seats = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM seats WHERE is_reserved = 1;')
    reserved_seats = cursor.fetchone()[0]

    print(f"\nReport:")
    print(f"Available seats: {available_seats}")
    print(f"Reserved seats: {reserved_seats}")

