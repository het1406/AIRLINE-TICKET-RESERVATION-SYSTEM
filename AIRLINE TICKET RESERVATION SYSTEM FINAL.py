import mysql.connector as mc

# Creating a MySQL database connection
mydb = mc.connect(host='localhost', user='root', passwd='root', database='airline_ticket_reservation_system')

# Creating a cursor object
mycursor = mydb.cursor()

# Accessing the database
mycursor.execute('USE airline_ticket_reservation_system')

# Function to display available flights
def display_flights():
    FLIGHTS = 'SELECT * FROM flights'
    mycursor.execute(FLIGHTS)
    myresult = mycursor.fetchall()
    
    header = 'S_No | flight_id | flight_number | departure  | destination | departure_date | available_seats'
    print(header)
    
    for row in myresult:
        print(row)

# Function to check seat availability for a flight
def check_seat_availability(flight_number):
    mycursor.execute('SELECT flight_id, available_seats FROM flights WHERE flight_number = %s', (flight_number,))
    row = mycursor.fetchone()
    
    if row:
        flight_id, available_seats = row
        print("Flight:", flight_number)
        print("Available Seats:", available_seats)
    else:
        print("Flight", flight_number, "not found.")

# Function to book a flight
def book_flight(flight_number, passenger_name):
    mycursor.execute('SELECT flight_id, available_seats FROM flights WHERE flight_number = %s', (flight_number,))
    row = mycursor.fetchone()

    if row:
        flight_id, available_seats = row
        if available_seats > 0:
            f_id = flight_id
            p_name = passenger_name
            seats = int(input('Enter the number of seats you want to book: '))
            seats1 = seats

            if seats <= available_seats:
                sql = 'INSERT INTO bookings (flight_id, passenger_name) VALUES (%s, %s)'
                val = (f_id, p_name)
                mycursor.execute(sql, val)
                
                update_sql = 'UPDATE flights SET available_seats = available_seats - %s WHERE flight_id = %s'
                update_val = (seats, f_id)
                mycursor.execute(update_sql, update_val)
                s = 'UPDATE bookings SET seats_booked = %s WHERE passenger_name = %s'
                update_seats = (seats1, p_name)
                mycursor.execute(s, update_seats)
         
                mydb.commit()
                succesful_booking()
            else:
                unsuccesful_booking()
        else:
            print("Sorry, this flight is fully booked.")
    else:
        print("Flight", flight_number, "not found.")

# Function to display a user's bookings
def display_bookings(passenger_name):
    mycursor.execute('SELECT flight_number FROM flights WHERE flight_id IN (SELECT flight_id FROM bookings WHERE passenger_name = %s)', (passenger_name,))
    booked_flights = mycursor.fetchall()
    
    if booked_flights:
        print("Booked Flights for", passenger_name)
        for flight in booked_flights:
            print(flight[0])
    else:
        print("No bookings found for", passenger_name)

# Function to cancel a user's bookings
def cancel_booking(passenger_name, flight_number):
    mycursor.execute('SELECT flight_id FROM flights WHERE flight_number = %s', (flight_number,))
    row = mycursor.fetchone()
    
    if row:
        flight_id = row[0]
        seats = int(input('Enter the number of seats you have booked: '))
        seats1 = seats
        mycursor.execute('DELETE FROM bookings WHERE flight_id = %s AND passenger_name = %s', (flight_id, passenger_name))
        mycursor.execute('UPDATE flights SET available_seats = available_seats + %s WHERE flight_id = %s', (seats1,flight_id,))
        mydb.commit()
        print("Booking for", passenger_name, "on flight", flight_number, "has been canceled.")
    else:
        print("Flight", flight_number, "not found.")

#Function to display successfull booking
def succesful_booking():
    print("Booking successful for your requested flight.")
    print('Thank you for booking with us.')
    print('We hope to see you again.')

#Function to display unsuccessfull booking for the requested number of seats
def unsuccesful_booking():
    print("Sorry, not enough seats available for your request.")

# Menu for user options
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Display Available Flights.")
        print("2. Check Seat Availability for a Flight.")
        print("3. Book a Flight.")
        print("4. Cancel Booking.")
        print("5. Display Your Bookings.")
        print("6. Exit.")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            display_flights()
        elif choice == '2':
            flight_number = input("Enter the flight number: ")
            check_seat_availability(flight_number)
        elif choice == '3':
            flight_number = input("Enter the flight number: ")
            passenger_name = input("Enter your name: ")
            book_flight(flight_number, passenger_name)
        elif choice == '4':
            passenger_name = input("Enter your name: ")
            flight_number = input("Enter the flight number to cancel: ")
            cancel_booking(passenger_name, flight_number)
        elif choice == '5':
            passenger_name = input("Enter your name: ")
            display_bookings(passenger_name)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please select a valid option.")

if _name_ == "_main_":
    main_menu()

# Closing the database connection
mydb.close()
