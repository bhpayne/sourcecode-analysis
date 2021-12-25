#!/usr/bin/env python3

"""
hello
"""

# https://realpython.com/python3-object-oriented-programming/
class Dog:
    pass

class Cat:
    # Class attribute
    species = "Canis familiaris"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    # Instance method
    def description(self):
        return f"{self.name} is {self.age} years old"

    # Another instance method
    def speak(self, sound):
        return f"{self.name} says {sound}"

class JackRussellTerrier(Cat):
    """
    great!
    """
    def speak(self, sound="Arf"):
        return f"{self.name} says {sound}"

class Dachshund(Dog):
    pass

