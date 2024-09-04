import mysql.connector

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="innovative"
        )
        return conn
    except mysql.connector.Error as err:
        print("Error:", err)

# user login
def login():
    hardcoded_username = "admin"
    hardcoded_password = "password"
    
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == hardcoded_username and password == hardcoded_password:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password. Please try again.")
        return False

# insertion
def insertion_menu(conn):
    cursor = conn.cursor()

    print("1. Insert into Owner table")
    print("2. Insert into Godown table")
    print("3. Insert into Employee table")
    print("4. Insert into Farmer table")
    print("5. Insert into Product table")
    print("6. Insert into Booking table")
    
    choice = input("Enter your choice: ")

    if choice == "1":
        owner_insertion(conn, cursor)
    elif choice == "2":
        godown_insertion(conn, cursor)
    elif choice == "3":
        employee_insertion(conn, cursor)
    elif choice == "4":
        farmer_insertion(conn, cursor)
    elif choice == "5":
        product_insertion(conn, cursor)
    elif choice == "6":
        booking_insertion(conn, cursor)
    else:
        print("Invalid choice.")

    conn.commit()
    cursor.close()

# Insertion function for Owner table
def owner_insertion(conn, cursor):
    print("Inserting into Owner table...")
    o_name = input("Enter owner name: ")
    o_contact = input("Enter owner contact: ")
    no_of_godown = int(input("Enter number of godowns owned: "))

    try:
        cursor.execute("INSERT INTO owner (O_Name, O_Contact, No_of_godown) VALUES (%s, %s, %s)",(o_name, o_contact, no_of_godown))
        print("Owner inserted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

# Insertion function for Godown table
def godown_insertion(conn, cursor):
    print("Inserting into Godown table...")
    g_city = input("Enter godown city: ")
    g_state = input("Enter godown state: ")
    capacity = int(input("Enter godown capacity: "))
    g_type = input("Enter godown type: ")
    owner_id = int(input("Enter owner ID: "))

    cursor.execute("SELECT Owner_id FROM owner WHERE Owner_id = %s", (owner_id,))
    result = cursor.fetchone()
    if result is None:
        print("Error: Owner with ID {} does not exist.".format(owner_id))
        return

    try:
        cursor.execute("INSERT INTO Godown (G_city, G_state, capacity, G_type, Owner_id) VALUES (%s, %s, %s, %s, %s)",
                       (g_city, g_state, capacity, g_type, owner_id))
        print("Godown inserted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

# Insertion function for Employee table
def employee_insertion(conn, cursor):
    print("Inserting into Employee table...")
    e_name = input("Enter employee name: ")
    e_contact = input("Enter employee contact: ")
    salary = int(input("Enter employee salary: "))
    joining_date = input("Enter employee joining date (YYYY-MM-DD): ")
    working_godown = int(input("Enter working godown ID: "))

    cursor.execute("SELECT Godown_id FROM Godown WHERE Godown_id = %s", (working_godown,))
    result = cursor.fetchone()
    if result is None:
        print("Error: Godown with ID {} does not exist.".format(working_godown))
        return

    try:
        cursor.execute("INSERT INTO employee (E_Name, E_Contact, Salary, joining_date, Working_Godown) VALUES (%s, %s, %s, %s, %s)",
                       (e_name, e_contact, salary, joining_date, working_godown))
        print("Employee inserted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

# Insertion function for Farmer table
def farmer_insertion(conn, cursor):
    print("Inserting into Farmer table...")
    f_name = input("Enter farmer name: ")
    f_contact = input("Enter farmer contact: ")
    f_city = input("Enter farmer city: ")
    f_state = input("Enter farmer state: ")

    try:
        cursor.execute("INSERT INTO Farmer (F_Name, F_Contact, F_City, F_state) VALUES (%s, %s, %s, %s)",
                       (f_name, f_contact, f_city, f_state))
        print("Farmer inserted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

# Insertion function for Product table
def product_insertion(conn, cursor):
    print("Inserting into Product table...")
    p_name = input("Enter product name: ")
    p_type = input("Enter product type: ")
    quantity = int(input("Enter product quantity: "))
    producer_id = int(input("Enter producer (farmer) ID: "))

    cursor.execute("SELECT Farmer_id FROM Farmer WHERE Farmer_id = %s", (producer_id,))
    result = cursor.fetchone()
    if result is None:
        print("Error: Farmer with ID {} does not exist.".format(producer_id))
        return

    try:
        cursor.execute("INSERT INTO Product (P_Name, P_type, quantity, producer) VALUES (%s, %s, %s, %s)",
                       (p_name, p_type, quantity, producer_id))
        print("Product inserted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

def booking_insertion(conn, cursor):
    print("Inserting into Booking table...")
    product_id = int(input("Enter product ID: "))
    godown_id = int(input("Enter godown ID: "))

    cursor.execute("SELECT Product_id, quantity FROM Product WHERE Product_id = %s", (product_id,))
    result_product = cursor.fetchone()
    if result_product is None:
        print("Error: Product with ID {} does not exist.".format(product_id))
        return
    product_quantity = result_product[1]

    cursor.execute("SELECT Godown_id, capacity FROM Godown WHERE Godown_id = %s", (godown_id,))
    result_godown = cursor.fetchone()
    if result_godown is None:
        print("Error: Godown with ID {} does not exist.".format(godown_id))
        return
    godown_capacity = result_godown[1]

    # Check if the product is already booked in the selected godown
    cursor.execute("SELECT * FROM Booking WHERE Product_id = %s AND Godown_id = %s", (product_id, godown_id))
    result_booking = cursor.fetchone()
    if result_booking:
        print("Error: Product with ID {} is already booked in godown with ID {}.".format(product_id, godown_id))
        return

    # Check if there is enough capacity in the godown
    cursor.execute("SELECT SUM(quantity) FROM Booking JOIN Product ON Booking.Product_id = Product.Product_id WHERE Godown_id = %s", (godown_id,))
    result_booked_quantity = cursor.fetchone()
    booked_quantity = result_booked_quantity[0] if result_booked_quantity[0] else 0

    if product_quantity + booked_quantity > godown_capacity:
        print("Error: Not enough capacity in godown with ID {}.".format(godown_id))
        return

    try:
        cursor.execute("INSERT INTO Booking (Product_id, Godown_id) VALUES (%s, %s)",(product_id, godown_id))
        print("Booking inserted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)


# deletion
def deletion_menu(conn):
    cursor = conn.cursor()

    print("1. Delete from Owner table")
    print("2. Delete from Godown table")
    print("3. Delete from Employee table")
    print("4. Delete from Farmer table")
    print("5. Delete from Product table")
    print("6. Delete from Booking table")

    choice = input("Enter your choice: ")

    if choice == "1":
        owner_deletion(conn, cursor)
    elif choice == "2":
        godown_deletion(conn, cursor)
    elif choice == "3":
        employee_deletion(conn, cursor)
    elif choice == "4":
        farmer_deletion(conn, cursor)
    elif choice == "5":
        product_deletion(conn, cursor)
    elif choice == "6":
        booking_deletion(conn, cursor)
    else:
        print("Invalid choice.")

    conn.commit()
    cursor.close()

def owner_deletion(conn, cursor):
    print("Deleting from Owner table...")
    owner_id = int(input("Enter owner ID to delete: "))

    try:
        # Get the IDs of godowns owned by the owner
        cursor.execute("SELECT Godown_id FROM Godown WHERE Owner_id = %s", (owner_id,))
        godown_ids = [row[0] for row in cursor.fetchall()]

        # Delete bookings associated with the godowns
        if godown_ids:
            placeholders = ', '.join(['%s'] * len(godown_ids))
            cursor.execute("DELETE FROM Booking WHERE Godown_id IN ({})".format(placeholders), godown_ids)

        # Delete employees working in the godowns
        if godown_ids:
            placeholders = ', '.join(['%s'] * len(godown_ids))
            cursor.execute("DELETE FROM Employee WHERE Working_Godown IN ({})".format(placeholders), godown_ids)

        # Delete godowns
        cursor.execute("DELETE FROM Godown WHERE Owner_id = %s", (owner_id,))

        # Delete owner
        cursor.execute("DELETE FROM Owner WHERE Owner_id = %s", (owner_id,))

        print("Owner and related records deleted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)


def godown_deletion(conn, cursor):
    print("Deleting from Godown table...")
    godown_id = int(input("Enter godown ID to delete: "))

    try:
        # Perform cascading delete in child tables
        cursor.execute("DELETE FROM Booking WHERE Godown_id = %s", (godown_id,))
        cursor.execute("DELETE FROM Godown WHERE Godown_id = %s", (godown_id,))
        print("Godown and related records deleted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

def employee_deletion(conn, cursor):
    print("Deleting from Employee table...")
    employee_id = int(input("Enter employee ID to delete: "))

    try:
        # Perform cascading delete in child tables
        cursor.execute("DELETE FROM employee WHERE Employee_id = %s", (employee_id,))
        print("Employee deleted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

def farmer_deletion(conn, cursor):
    print("Deleting from Farmer table...")
    farmer_id = int(input("Enter farmer ID to delete: "))

    try:
        # Delete products of the farmer from Booking table
        cursor.execute("DELETE FROM Booking WHERE Product_id IN (SELECT Product_id FROM Product WHERE producer = %s)", (farmer_id,))
        
        # Perform cascading delete in child tables
        cursor.execute("DELETE FROM Product WHERE producer = %s", (farmer_id,))
        cursor.execute("DELETE FROM Farmer WHERE Farmer_id = %s", (farmer_id,))
        
        print("Farmer, related products, and bookings deleted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

def product_deletion(conn, cursor):
    print("Deleting from Product table...")
    product_id = int(input("Enter product ID to delete: "))

    try:
        # Perform cascading delete in child tables
        cursor.execute("DELETE FROM Booking WHERE Product_id = %s", (product_id,))
        cursor.execute("DELETE FROM Product WHERE Product_id = %s", (product_id,))
        print("Product and related records deleted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

def booking_deletion(conn, cursor):
    print("Deleting from Booking table...")
    booking_id = int(input("Enter booking ID to delete: "))

    try:
        # Perform cascading delete in child tables
        cursor.execute("DELETE FROM Booking WHERE Booking_id = %s", (booking_id,))
        print("Booking deleted successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)


def product_update(conn, cursor):
    print("Updating Product table...")
    product_id = int(input("Enter product ID to update: "))
    new_name = input("Enter new product name: ")
    new_type = input("Enter new product type: ")
    new_quantity = int(input("Enter new product quantity: "))
    new_producer_id = int(input("Enter new producer (farmer) ID: "))

    # Check if farmer exists
    cursor.execute("SELECT Farmer_id FROM Farmer WHERE Farmer_id = %s", (new_producer_id,))
    result = cursor.fetchone()
    if result is None:
        print("Error: Farmer with ID {} does not exist.".format(new_producer_id))
        return

    # Update Product table
    try:
        cursor.execute("UPDATE Product SET P_Name = %s, P_type = %s, quantity = %s, producer = %s WHERE Product_id = %s",
                       (new_name, new_type, new_quantity, new_producer_id, product_id))
        print("Product updated successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

def booking_update(conn, cursor):
    print("Updating Booking table...")
    booking_id = int(input("Enter booking ID to update: "))
    new_product_id = int(input("Enter new product ID: "))
    new_godown_id = int(input("Enter new godown ID: "))

    # Check if product exists
    cursor.execute("SELECT Product_id FROM Product WHERE Product_id = %s", (new_product_id,))
    result_product = cursor.fetchone()
    if result_product is None:
        print("Error: Product with ID {} does not exist.".format(new_product_id))
        return

    # Check if godown exists
    cursor.execute("SELECT Godown_id FROM Godown WHERE Godown_id = %s", (new_godown_id,))
    result_godown = cursor.fetchone()
    if result_godown is None:
        print("Error: Godown with ID {} does not exist.".format(new_godown_id))
        return

    # Update Booking table
    try:
        cursor.execute("UPDATE Booking SET Product_id = %s, Godown_id = %s WHERE Booking_id = %s",(new_product_id, new_godown_id, booking_id))
        print("Booking updated successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)


# update
def update_menu(conn):
    cursor = conn.cursor()

    print("1. Update Owner table")
    print("2. Update Godown table")
    print("3. Update Employee table")
    print("4. Update Farmer table")
    print("5. Update Product table")
    print("6. Update Booking table")

    choice = input("Enter your choice: ")

    if choice == "1":
        owner_update(conn, cursor)
    elif choice == "2":
        godown_update(conn, cursor)
    elif choice == "3":
        employee_update(conn, cursor)
    elif choice == "4":
        farmer_update(conn, cursor)
    elif choice == "5":
        product_update(conn, cursor)
    elif choice == "6":
        booking_update(conn, cursor)
    else:
        print("Invalid choice.")

    conn.commit()
    cursor.close()

def owner_update(conn, cursor):
    print("Updating Owner table...")
    owner_id = int(input("Enter owner ID to update: "))
    new_name = input("Enter new owner name: ")
    new_contact = input("Enter new owner contact: ")

    # Update Owner table
    try:
        cursor.execute("UPDATE Owner SET O_Name = %s, O_Contact = %s WHERE Owner_id = %s",(new_name, new_contact, owner_id))
        print("Owner updated successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

def godown_update(conn, cursor):
    print("Updating Godown table...")
    godown_id = int(input("Enter godown ID to update: "))
    new_city = input("Enter new city: ")
    new_state = input("Enter new state: ")
    new_capacity = int(input("Enter new capacity: "))
    new_type = input("Enter new type: ")

    # Update Godown table
    try:
        cursor.execute("UPDATE Godown SET G_city = %s, G_state = %s, capacity = %s, G_type = %s WHERE Godown_id = %s",(new_city, new_state, new_capacity, new_type, godown_id))
        print("Godown updated successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

def employee_update(conn, cursor):
    print("Updating Employee table...")
    employee_id = int(input("Enter employee ID to update: "))
    new_name = input("Enter new employee name: ")
    new_contact = input("Enter new employee contact: ")
    new_salary = int(input("Enter new employee salary: "))
    new_joining_date = input("Enter new joining date (YYYY-MM-DD): ")

    # Update Employee table
    try:
        cursor.execute("UPDATE Employee SET E_Name = %s, E_Contact = %s, Salary = %s, joining_date = %s WHERE Employee_id = %s",(new_name, new_contact, new_salary, new_joining_date, employee_id))
        print("Employee updated successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

def farmer_update(conn, cursor):
    print("Updating Farmer table...")
    farmer_id = int(input("Enter farmer ID to update: "))
    new_name = input("Enter new farmer name: ")
    new_contact = input("Enter new farmer contact: ")
    new_city = input("Enter new farmer city: ")
    new_state = input("Enter new farmer state: ")
    # Update Farmer table
    try:
        cursor.execute("UPDATE Farmer SET F_Name = %s, F_Contact = %s, F_City = %s, F_state = %s WHERE Farmer_id = %s",(new_name, new_contact, new_city, new_state, farmer_id))
        print("Farmer updated successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

   
def display_table_menu(conn):
    cursor = conn.cursor()

    while True:
        print("\nMenu:")
        print("1. Display Owner table")
        print("2. Display Godown table")
        print("3. Display Employee table")
        print("4. Display Farmer table")
        print("5. Display Product table")
        print("6. Display Booking table")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_table(conn, "Owner")
        elif choice == "2":
            display_table(conn, "Godown")
        elif choice == "3":
            display_table(conn, "Employee")
        elif choice == "4":
            display_table(conn, "Farmer")
        elif choice == "5":
            display_table(conn, "Product")
        elif choice == "6":
            display_table(conn, "Booking")
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    cursor.close()

def display_table(conn, table_name):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM {}".format(table_name))
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        if rows:
            print("\n{} Table:".format(table_name))
            print("-" * 30)
            for col in columns:
                print(col, end='\t')
            print("\n" + "-" * 30)
            for row in rows:
                for val in row:
                    print(val, end='\t')
                print()
            print("-" * 30)
        else:
            print("No data found in {} table.".format(table_name))
    except mysql.connector.Error as err:
        print("Error:", err)


# Main function
def main():
    conn = connect_to_database()
    if conn is None:
        return

    logged_in = False
    while not logged_in:
        logged_in = login()
    
    while True:
        print("\nMenu:")
        print("1. Insertion")
        print("2. Deletion")
        print("3. Update")
        print("4. Display")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            insertion_menu(conn)
        elif choice == "2":
            deletion_menu(conn)
        elif choice == "3":
            update_menu(conn)
        elif choice == "4":
            display_table_menu(conn)
        elif (choice == "5"):
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()


main()