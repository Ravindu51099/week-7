from abc import ABC, abstractmethod


# ==========================================================
# Abstract Factory
# Defines a common interface for all factory classes.
# ==========================================================
class Factory(ABC):

    @abstractmethod
    def create_product(self):
        pass


# ==========================================================
# Concrete Factory: DogFactory
# Responsible for creating Dog objects.
# ==========================================================
class DogFactory(Factory):

    def create_product(self):
        return Dog()


# ==========================================================
# Concrete Factory: CatFactory
# Responsible for creating Cat objects.
# ==========================================================
class CatFactory(Factory):

    def create_product(self):
        return Cat()


# ==========================================================
# Abstract Product
# Defines a common interface for all animal types.
# ==========================================================
class Animals(ABC):

    @abstractmethod
    def run(self):
        pass


# ==========================================================
# Concrete Product: Dog
# Implements the run() method for a Dog.
# ==========================================================
class Dog(Animals):

    def run(self):
        print("I'm a Dog, I can run!!")


# ==========================================================
# Concrete Product: Cat
# Implements the run() method for a Cat.
# ==========================================================
class Cat(Animals):

    def run(self):
        print("I'm a Cat, I can run!!")


# ==========================================================
# Client Code
# ==========================================================

# Create an instance of DogFactory.
# The client does not directly create a Dog object.
factory = DogFactory()

# Request the factory to create a product.
# DogFactory creates and returns a Dog object.
dog = factory.create_product()

# Execute the Dog object's behaviour.
# The run() method from the Dog class is called.
dog.run()

# ==========================================================
# Outcome of the Implementation
# ==========================================================
#
# 1. The client creates a DogFactory object.
#
# 2. The client requests a product by calling:
#       factory.create_product()
#
# 3. DogFactory creates and returns a Dog object.
#
# 4. The Dog object is stored in the variable 'dog'.
#
# 5. The client calls:
#       dog.run()
#
# 6. The Dog class implementation of run() executes and prints:
#
#       I'm a Dog, I can run!!
#
# Expected Output:
#
# I'm a Dog, I can run!!
#
# This implementation demonstrates the Factory Design Pattern
# because object creation is delegated to a factory class rather
# than being performed directly by the client. This makes the
# code easier to maintain, extend, and modify. New animal types
# can be added by creating new product classes and factory
# classes without changing the client code.
#
# ==========================================================