import sqlite3
from abc import ABC, abstractmethod


# ==========================================================
# Singleton Database Class
# Only one database connection is created and reused.
# ==========================================================
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect("aquarium.db")
            cls._instance.cursor = cls._instance.connection.cursor()
        return cls._instance

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS fish (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)
        self.connection.commit()

    def insert_fish(self, name, category, quantity):
        self.cursor.execute("""
            INSERT INTO fish (name, category, quantity)
            VALUES (?, ?, ?)
        """, (name, category, quantity))
        self.connection.commit()

    def display_fish(self):
        self.cursor.execute("SELECT name, category, quantity FROM fish")
        records = self.cursor.fetchall()

        print("\n===== Auckland Aquarium Fish List =====")

        if not records:
            print("No fish records available.")
        else:
            for fish in records:
                print(f"Fish Name: {fish[0]}")
                print(f"Category : {fish[1]}")
                print(f"Quantity : {fish[2]}")
                print("----------------------------------")


# ==========================================================
# Abstract Fish Class
# ==========================================================
class Fish(ABC):

    @abstractmethod
    def get_category(self):
        pass


# ==========================================================
# Concrete Fish Classes
# ==========================================================
class Goldfish(Fish):
    def get_category(self):
        return "Freshwater Fish"


class Shark(Fish):
    def get_category(self):
        return "Marine Predator Fish"


class Angelfish(Fish):
    def get_category(self):
        return "Tropical Fish"


class Tuna(Fish):
    def get_category(self):
        return "Marine Fish"


class Salmon(Fish):
    def get_category(self):
        return "Migratory Fish"


# ==========================================================
# Factory Pattern
# Creates fish objects based on user input.
# ==========================================================
class FishFactory:

    @staticmethod
    def create_fish(fish_name):
        fish_name = fish_name.lower()

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
        else:
            return None


# ==========================================================
# Main Program
# ==========================================================
def main():
    database = DatabaseConnection()
    database.create_table()

    while True:
        print("\n===== Auckland Aquarium Management System =====")
        print("1. Add Fish")
        print("2. Display Fish")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            fish_name = input("Enter fish name Goldfish/Shark/Angelfish/Tuna/Salmon: ")
            fish = FishFactory.create_fish(fish_name)

            if fish is None:
                print("Invalid fish type.")
            else:
                quantity = int(input("Enter number of fish available: "))
                category = fish.get_category()

                database.insert_fish(fish_name, category, quantity)
                print("Fish record added successfully.")

        elif choice == "2":
            database.display_fish()

        elif choice == "3":
            print("Exiting Auckland Aquarium Management System.")
            break

        else:
            print("Invalid choice. Please try again.")


main()