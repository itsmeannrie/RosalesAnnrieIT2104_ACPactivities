from Capybara import Capybara

capybaras = [
    Capybara("Biscoff", "M", 5),
    Capybara("Solara", "F", 3),
    Capybara("ALas", "M", 7),
    Capybara("Koko", "F", 4)
]

test_case = int(input("Enter the test case number: "))

if 1 <= test_case <= len(capybaras):
    print(f"Test Case {test_case}: {capybaras[test_case - 1].display()}")
else:
    print("Invalid test case number.")