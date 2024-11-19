def perfect_num(number):
    divisors_sum = sum(i for i in range(1, number) if number % i == 0)
    return divisors_sum == number

def main():
    try:
        number = int(input("Enter a number: "))
        if perfect_num(number):
            print(f"{number} is a perfect number.")
        else:
            print(f"{number} is not a perfect number.")
    except ValueError:
        print("Please enter a valid integer.")

if __name__ == "__main__":
    main()
