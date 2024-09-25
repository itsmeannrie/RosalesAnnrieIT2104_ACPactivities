while True:
    purchase_amount = float(input("Enter the total purchase amount: "))

    if purchase_amount > 5000:
        discount = purchase_amount * 0.10 
    else:
        discount = purchase_amount * 0.05 

 
    final_price = purchase_amount - discount
    print(f"Initial Purchase Amount: {purchase_amount:.2f}")
    print(f"Discount: {discount:.2f}")  
    print(f"Final price: {final_price:.2f}")

    user_response = input("Do you want to try again? (yes/no): ").lower()
    if user_response != 'yes':
        print("Thank you!")
        break
