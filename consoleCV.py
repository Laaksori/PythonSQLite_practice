# Python practice project by Riku Laakso
# Creating a pdf-cv is not too thrilling, so by creating a programmed version I at least have an idea what to include in the cv
# Also good practice to create a program with a language I'm not so familiar with
import sqlite3 as sql
from urllib.request import pathname2url

# create tables and insert data into them
def create_database():
    connection = sql.connect(":memory:") # no need to create a file since all of the data is hardcoded for practice
    cur = connection.cursor()

    #education table and data inserts
    cur.execute(
        """CREATE TABLE IF NOT EXISTS education(
            id INTEGER PRIMARY KEY,
            degree TEXT NOT NULL,
            school TEXT NOT NULL,
            start_year INTEGER NOT NULL,
            end_year INTEGER
            )"""
    )

    cur.execute(
        """
                INSERT INTO education (degree, school, start_year, end_year)
            VALUES(?,?,?,?) """,
        ("Peliala", "Riveria, Outokumpu", 2018, 2020),
    )

    # separate insert because less data
    cur.execute(
        """
                INSERT INTO education (degree, school, start_year)
            VALUES(?,?,?) """,
        ("GameProgramming", "XAMK, Kotka", 2021),
    )

    # work experience table and data inserts
    cur.execute(
        """CREATE TABLE IF NOT EXISTS workexperience(
            id INTEGER PRIMARY KEY, 
            company TEXT NOT NULL,
            description TEXT NOT NULL,
            duration TEXT
            )"""
    )

    cur.executemany(
        """
                INSERT INTO workexperience (company, description, duration)
                VALUES(?,?,?)
                """,
        [
            ("Innocode", "Developer", "10/2024 - 1/2025"),
            ("UglySwan", "UnityProgramming", "5/2025-8/2025"),
        ],
    )

    #hobbies table and data
    cur.execute(
        """CREATE TABLE IF NOT EXISTS hobbies(
            id INTEGER PRIMARY KEY, 
            hobby TEXT NOT NULL,
            description TEXT NOT NULL
            )"""
    )

    cur.executemany(
        """
                INSERT INTO hobbies (hobby, description)
                VALUES(?,?)
                """,
        [
            (
                "3D-printing",
                "Designing and printing (mostly) useful objects. Using Blender to 3D model. I try to keep my designs efficient to avoid waste and maximize resources",
            ),
            (
                "Tinkering",
                "All kinds of small tinkering, such as repairing/deconstructing electronics to learn about them. Creating lights, everyday helpful items, learning how to use microcontrollers",
            ),
        ],
    )

    # about me table and data
    cur.execute(
        """CREATE TABLE IF NOT EXISTS about(
            id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL,
            age TEXT NOT NULL,
            location TEXT NOT NULL,
            email TEXT NOT NULL,
            phonenumber TEXT NOT NULL
            )"""
    )

    cur.execute(
        """
                INSERT INTO about (name, age, location, email, phonenumber)
            VALUES(?,?,?,?,?) """,
        ("Redacted", "Redacted", "Redacted", "Redacted", "Redacted"),
    )
    return connection, cur

# function to take user input to choose a table
def select_table(cur):
    print("Enter index of the table you want to view. 0 will exit the program")

    for i, (name,) in enumerate(
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'"), start=1):
            print(f"{i} {name}")

    while True:
        try:
            index = int(input("Index: "))
        except ValueError:
            print("Please enter an integer in range 0-4")
        else:
            break
    
    chosentable = "default"

    match index:
        case 1:
            print("Selected education")
            chosentable = "education"
        case 2:
            print("Selected work experience")
            chosentable = "workexperience"
        case 3:
            print("Selected hobbies")
            chosentable = "hobbies"
        case 4:
            print("Selected about")
            chosentable = "about"
        case 0:
            return None
        case _:
            print("Invalid index")

    print()
    return chosentable

# show the table that was chosen with select_table
def show_table(cur, chosentable):

    if chosentable == "default":
        return 
    cur.execute(f"SELECT * FROM {chosentable}")
    col_names = [desc[0] for desc in cur.description]  # get column names
    rows = cur.fetchall()

    for row_num, row in enumerate(rows, start=1):
        for col, value in zip(col_names, row):
            if col == "id":
                continue
            print(f"  {col}: {value}")
        print()

# main function 
def mainloop():
    connection, cur = create_database() #create the database and return connection and cursor

    # loop selection and show until the user gets bored
    while True:
        chosentable = select_table(cur)
        if chosentable is None:
            print("Exiting program")
            break
        elif chosentable == "default":
            continue

        show_table(cur, chosentable)

    connection.close() # close the connection (which is probably not needed as the database is temporary)

# run mainloop
mainloop()