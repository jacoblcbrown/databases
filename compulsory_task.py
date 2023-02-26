# ===== Compulsory Task =====

# ===== Imports =====
import sqlite3


# ===== Functions =====
# This function prints all books in the database.
def view_all():
    cursor.execute('''SELECT * FROM books''')

    for row in cursor:
        print(f"ID: {row[0]}\n"
              f"TITLE: {row[1]}\n"
              f"AUTHOR: {row[2]}\n"
              f"QTY: {row[3]}\n"
              "===============================================================")


# This function prints the books in the database and then requests the book ID. This is returned to respective section
# and used to either update or delete a book.
def book_selector():
    print("The books below are currently in the database:\n")

    view_all()

    cursor.execute('''SELECT * FROM books''')

    # Input validation check - part 1 of 2.
    acceptable_ids = []

    for row in cursor:
        acceptable_ids.append(row[0])

    while True:
        try:
            # Input request.
            book_id = int(input("\nPlease enter the book ID: "))

            # Input validation check - part 2 of 2.
            if book_id in acceptable_ids:
                break

            else:
                print("That ID does not exist. Please try again.")

        except ValueError:
            print("That ID does not exist. Please try again.")

    return book_id


# === Classes ===
# Custom exception; raised when incorrect menu input used.
class NotMenuInputException(Exception):
    "NotMenuInput: Your menu input is not recognised. Please try again."
    pass


# ===== Variables =====
acceptable_menu_inputs = ["e", "u", "d", "s", "v", "x"]

# === Database connection ===
# Creating a database and making a connection to it.
db = sqlite3.connect('ebookstore_db')
cursor = db.cursor()

# Creating a table.
"""Try/except used for purpose of task. Ensures fresh table created regardless of where program stopped
# on previous run."""
try:
    cursor.execute('''DROP TABLE books''')

except Exception:
    pass

cursor.execute('''CREATE TABLE books(id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)''')

# Inserting rows into the table.
books = [[3001, 'A Tale of Two Cities', 'Charles Dickens', 30],
         [3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40],
         [3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25],
         [3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37],
         [3005, 'Alice in Wonderland', 'Lewis Carroll', 12]]

cursor.executemany(''' INSERT INTO books(id, title, author, qty) VALUES(?,?,?,?)''', books)

# === main program code ===
print("   ***  Welcome to the ebookstore!  ***")

while True:

    while True:
        menu = input("==========================================\n"
                     "                 MAIN MENU\n"
                     "==========================================\n"
                     "Select one of the following options below:\n"
                     "e  - Enter book\n"
                     "u  - Update book\n"
                     "d - Delete book\n"
                     "s - Search books\n"
                     "v - View database\n"
                     "x  - Exit\n"
                     "\nEnter here: ").lower()

        # Input validation check.
        try:
            if menu not in acceptable_menu_inputs:
                raise NotMenuInputException

            else:
                break

        except NotMenuInputException:
            print("Your menu input is not recognised. Please try again.\n")

    # === Add a book to the database section ===
    # In this section, the user can add a book to the database.
    if menu == 'e':

        title, author, qty = input("Please enter the book title (t), author (a) and quantity (q) "
                                   "(format: t,a,q): ").split(",")

        cursor.execute('''INSERT INTO books(title, author, qty) VALUES(?,?,?)''', (title, author, int(qty)))

        print("\nBook successfully added.\n")

    # === Update a book to the database section ===
    # In this section, a user can update book information in the database.
    elif menu == 'u':
        book_id = book_selector()

        while True:
            menu = input("\nEnter the option of the information you would like to update:\n"
                         "t  - title\n"
                         "a - author\n"
                         "q - qty\n"
                         "x - exit\n"
                         "\nEnter here: ").lower()

            if menu == "t":
                title = input("Please enter the updated title: ")
                cursor.execute('''UPDATE books SET title = ? WHERE id = ? ''', (title, book_id))
                print("\nBook successfully updated.\n")

                break

            elif menu == "a":
                author = input("Please enter the updated author: ")
                cursor.execute('''UPDATE books SET author = ? WHERE id = ? ''', (author, book_id))
                print("\nBook successfully updated.\n")

                break

            elif menu == "q":
                qty = input("Please enter the updated qty: ")
                cursor.execute('''UPDATE books SET qty = ? WHERE id = ? ''', (qty, book_id))
                print("\nBook successfully updated.\n")

                break

            elif menu == "x":
                break

            else:
                print("Input not recognised. Please try again.")    # Input validation check.

    # === Delete a book in the database section ===
    # In this section, a user can delete a book from the database.
    elif menu == 'd':
        book_id = book_selector()

        cursor.execute('''DELETE FROM books WHERE id = ? ''', (book_id,))

        print("\nBook successfully deleted.\n")

    # === Search for a book in the database section ===
    # In this section, a user can search for a book using the author or title. It will then print the results. This
    # search uses both a prefix and suffix wildcard and so accepts partial matches.
    elif menu == 's':

        search_term = input("Please enter your search term: ")

        search_term = "%" + search_term + "%"

        cursor.execute('''SELECT * FROM books WHERE title like ? OR author like ? ''', (search_term, search_term))

        print("\n                     ***   SEARCH RESULTS   ***\n"
              "===============================================================")

        for row in cursor:
            print(f"ID: {row[0]}\n"
                  f"TITLE: {row[1]}\n"
                  f"AUTHOR: {row[2]}\n"
                  f"QTY: {row[3]}\n"
                  "===============================================================")

    # === View the database section ===
    # In this section, the user can print out the entire database.
    elif menu == 'v':
        cursor.execute('''SELECT * FROM books''')

        print("\n                     ***   DATABASE   ***\n"
              "===============================================================")

        view_all()

    # === Exit the database section ===
    # In this section, the user can exit the program.
    elif menu == 'x':
        print("\nYou have successfully exited the ebookstore!")

        # Committing all changes and closing the database connection.
        db.commit()
        db.close()
        break
