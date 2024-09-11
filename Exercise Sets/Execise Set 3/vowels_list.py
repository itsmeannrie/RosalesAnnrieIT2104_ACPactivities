string = input("Enter a string: ")
vowels = "aeiouAEIOU"
vowels_list= []

for char in string:
    if char in vowels:
        vowels_list.append(char)

print(vowels_list)