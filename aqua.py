# Import SQLite for database operations
import sqlite3

# Import ABC and abstractmethod to create abstract classes
from abc import ABC, abstractmethod


# ==========================================================
# Singleton Database Class
# ==========================================================
# This class implements the Singleton Design Pattern.
# The purpose is to ensure that only ONE database connection
# exists throughout the entire application.
# ==========================================================
class DatabaseConnection:

    # Stores the single instance of the class
    _instance = None

    # __new__ is called before __init__
    # It controls object creation
    def __new__(cls):

        # If no instance exists yet, create one
        if cls._instance is None:

            # Create the object
            cls._instance = super(DatabaseConnection, cls).__new__(cls)

            # Create a connection to SQLite database
            # If aquarium.db does not exist, it will be created automatically
            cls._instance.connection = sqlite3.connect("aquarium.db")

            # Create a cursor object used to execute SQL queries
            cls._instance.cursor = cls._instance.connection.cursor()

        # Return the existing instance
        return cls._instance

    # Create the fish table if it does not already exist
    def create_table(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fish (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)

        # Save changes to the database
        self.connection.commit()

    # Insert a fish record into the database
    def insert_fish(self, name, category, quantity):

        self.cursor.execute("""
            INSERT INTO fish (name, category, quantity)
            VALUES (?, ?, ?)
        """, (name, category, quantity))

        # Save the inserted record
        self.connection.commit()

    # Display all fish records stored in the database
    def display_fish(self):

        # Retrieve all fish records
        self.cursor.execute(
            "SELECT name, category, quantity FROM fish"
        )

        # Store query results
        records = self.cursor.fetchall()

        print("\n===== Auckland Aquarium Fish List =====")

        # If table is empty
        if not records:
            print("No fish records available.")

        # Display all records
        else:
            for fish in records:

                print(f"Fish Name: {fish[0]}")
                print(f"Category : {fish[1]}")
                print(f"Quantity : {fish[2]}")
                print("----------------------------------")


# ==========================================================
# Abstract Fish Class
# ==========================================================
# This acts as the parent class for all fish types.
# Every fish must implement get_category().
# ==========================================================
class Fish(ABC):

    @abstractmethod
    def get_category(self):
        pass


# ==========================================================
# Concrete Fish Classes
# ==========================================================
# Each fish type inherits from Fish and provides its own
# category description.
# ==========================================================

class Goldfish(Fish):

    # Returns the category of Goldfish
    def get_category(self):
        return "Freshwater Fish"


class Shark(Fish):

    # Returns the category of Shark
    def get_category(self):
        return "Marine Predator Fish"


class Angelfish(Fish):

    # Returns the category of Angelfish
    def get_category(self):
        return "Tropical Fish"


class Tuna(Fish):

    # Returns the category of Tuna
    def get_category(self):
        return "Marine Fish"


class Salmon(Fish):

    # Returns the category of Salmon
    def get_category(self):
        return "Migratory Fish"


# ==========================================================
# Factory Pattern
# ==========================================================
# FishFactory is responsible for creating fish objects.
# The client code does not directly create Goldfish(),
# Shark(), etc.
#
# Instead it asks the factory to create the correct fish
# object based on user input.
# ==========================================================
class FishFactory:

    @staticmethod
    def create_fish(fish_name):

        # Convert user input to lowercase
        # so matching becomes case-insensitive
        fish_name = fish_name.lower()

        # Create and return the correct fish object

        if fish_name == "goldfish":
            return Goldfish()

        elif fish_name == "shark":
            return Shark()

        elif fish_name == "angelfish":
            return Angelfish()

        elif fish_name == "tuna":
            return Tuna()

        elif fish_name == "salmon":
            return Salmon()

        # Invalid fish type
        else:
            return None


# ==========================================================
# Main Program
# ==========================================================
# Controls the menu system and user interaction.
# ==========================================================
def main():

    # Create database object
    # Because of Singleton Pattern, only one database
    # connection object will ever exist.
    database = DatabaseConnection()

    # Create fish table if it doesn't exist
    database.create_table()

    # Infinite loop for menu
    while True:

        print("\n===== Auckland Aquarium Management System =====")
        print("1. Add Fish")
        print("2. Display Fish")
        print("3. Exit")

        # Get user choice
        choice = input("Enter your choice: ")

        # ==================================================
        # Option 1 - Add Fish
        # ==================================================
        if choice == "1":

            # Ask user for fish type
            fish_name = input(
                "Enter fish name Goldfish/Shark/Angelfish/Tuna/Salmon: "
            )

            # Use Factory Pattern to create fish object
            fish = FishFactory.create_fish(fish_name)

            # Invalid fish entered
            if fish is None:
                print("Invalid fish type.")

            else:
                # Ask for quantity
                quantity = int(
                    input("Enter number of fish available: ")
                )

                # Get category from fish object
                category = fish.get_category()

                # Store record in database
                database.insert_fish(
                    fish_name,
                    category,
                    quantity
                )

                print("Fish record added successfully.")

        # ==================================================
        # Option 2 - Display Fish Records
        # ==================================================
        elif choice == "2":

            # Retrieve and display all fish records
            database.display_fish()

        # ==================================================
        # Option 3 - Exit Program
        # ==================================================
        elif choice == "3":

            print(
                "Exiting Auckland Aquarium Management System."
            )

            break

        # ==================================================
        # Invalid Menu Option
        # ==================================================
        else:
            print("Invalid choice. Please try again.")


# ==========================================================
# Program Entry Point
# ==========================================================
# Starts execution of the application.
# ==========================================================
main()


# ==========================================================
# HOW THE SINGLETON PATTERN IS USED
# ==========================================================
# DatabaseConnection ensures only one SQLite connection
# object exists throughout the application.
#
# Every time DatabaseConnection() is called, the same object
# is returned instead of creating a new database connection.
#
# This reduces resource usage and centralizes database access.
#
# Example:
#
# db1 = DatabaseConnection()
# db2 = DatabaseConnection()
#
# print(db1 is db2)
#
# Output:
# True
#
# This proves both variables refer to the same object.
# ==========================================================


# ==========================================================
# HOW THE FACTORY PATTERN IS USED
# ==========================================================
# FishFactory creates fish objects based on the fish name
# entered by the user.
#
# Instead of directly creating:
#
# fish = Shark()
#
# the client uses:
#
# fish = FishFactory.create_fish("Shark")
#
# The factory determines which object should be created and
# returns the correct fish object.
#
# This separates object creation from business logic and
# makes the system easier to extend in the future.
# ==========================================================