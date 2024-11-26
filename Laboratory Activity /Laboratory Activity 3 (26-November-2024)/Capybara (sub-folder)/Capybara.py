class Capybara:
    def __init__(self, name: str, gender: str, age: int):
        self.name = name
        self.gender = gender
        self.age = age

    def display(self):
        return f"Name: {self.name}, Gender: {self.gender}, Age: {self.age} years old"
