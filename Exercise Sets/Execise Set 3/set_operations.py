set1 = {8, 16, 24, 32, 44}
set2 = {7, 14, 8, 32, 21}

# Set Difference
set_difference1 = set1 - set2  
set_difference2 = set2 - set1  

# Union Sets
set_union = set1 | set2  

# Symmetric Difference
symmetric_difference1 = set2 ^ set1  
symmetric_difference2 = set1 ^ set2  

# Set Intersection
intersection_set1 = set1 & set2  
intersection_set2 = set2 & set1

print("Set Difference (set1 - set2):", set_difference1)
print("Set Difference (set2 - set1):", set_difference2)
print("\nUnion of Sets (set1 | set2):", set_union)
print("Symmetric Difference (set2 ^ set1):", symmetric_difference1)
print("Symmetric Difference (set1 ^ set2):", symmetric_difference2)
print("\nSet Intersection (set1 & set2):", intersection_set1)
print("Set Intersection (set2 & set1):", intersection_set2)