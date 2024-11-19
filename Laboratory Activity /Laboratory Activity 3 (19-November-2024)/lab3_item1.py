def roman_to_integer(roman):
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev = 0
    
    for char in reversed(roman.upper()):  
        if char in roman_values:
            current = roman_values[char]
            if current < prev:
                total -= current  
            else:
                total += current  
            prev = current
        else:
            return None  
        
    return total

def main():
    roman = input("Enter a Roman numeral: ")
    result = roman_to_integer(roman)
    
    if result is not None:
        print(f"The integer value of '{roman.upper()}' is: {result}")
    else:
        print("Invalid Roman numeral input.")

if __name__ == "__main__":
    main()
    
