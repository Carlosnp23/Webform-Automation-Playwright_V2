import mysql.connector

# ---------- Connect to the database ----------
try:
    conn = mysql.connector.connect(
        host="switchback.proxy.rlwy.net",  # Railway host
        port=40842,                        # Railway port
        user="root",                        # Railway username
        password="hpDkeofzJSiakVbpmozJZVMSpUCbIOca",  # Railway password
        database="railway"                  # Railway database name
    )
    cursor = conn.cursor()  # Create a cursor for executing queries
    print("Connected to the database successfully!")

except mysql.connector.Error as err:
    print("Error connecting to database:", err)
    exit()

# ---------- Create table if it does not exist ----------
create_table_query = """
CREATE TABLE IF NOT EXISTS users_v2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Email VARCHAR(100),
    Gender VARCHAR(10),
    Date_of_Birth DATE,
    Subjects TEXT,
    Hobbies TEXT,
    Picture VARCHAR(255),
    Current_Address TEXT,
    State_and_City VARCHAR(100)
);
"""

try:
    cursor.execute(create_table_query)
    print("Table 'users_v2' is ready.")

except mysql.connector.Error as err:
    print("Error creating table:", err)

# ---------- Insert sample records ----------
insert_query = """
INSERT INTO users_v2
(First_Name, Last_Name, Email, Gender, Date_of_Birth, Subjects, Hobbies, Picture, Current_Address, State_and_City)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

values = [
    ("Carlos", "Noram", "carlos@email.com", "Male", "1995-07-14",
     "Math, Physics", "Reading, Football", "profile1.jpg", "123 Main St", "Toronto, ON"),
    
    ("Lucia", "Martinez", "lucia@email.com", "Female", "1998-03-22",
     "History, Literature", "Music, Painting", "profile2.jpg", "456 Queen St", "Vancouver, BC")
]

try:
    cursor.executemany(insert_query, values)  # Insert multiple records
    conn.commit()  # Commit the transaction
    print(cursor.rowcount, "records inserted successfully!")

except mysql.connector.Error as err:
    print("Error inserting records:", err)
    conn.rollback()  # Rollback in case of error

# ---------- Fetch and display data ----------
try:
    cursor.execute("SELECT * FROM users_v2;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except mysql.connector.Error as err:
    print("Error fetching data:", err)

# ---------- Close connection ----------
cursor.close()
conn.close()
print("Database connection closed.")

