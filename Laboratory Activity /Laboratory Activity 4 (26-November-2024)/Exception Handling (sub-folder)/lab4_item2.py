size = int(input("Enter the size of the array: "))
arr = [0.0] * size  

print("Enter the elements of the array:")
for i in range(size):
    arr[i] = float(input())  

j = int(input("Enter the index of the element to print: "))
try:
    print(f"{arr[j]:.2f}") 
except IndexError:
    print(f"Index {j} is invalid.")  
