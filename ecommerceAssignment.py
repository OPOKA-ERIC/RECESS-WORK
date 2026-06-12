# E-Commerce System

print("========== E-COMMERCE SYSTEM ==========")

# LOGIN SECTION
username = input("Enter username: ")
password = input("Enter password: ")

# Check credentials
if username == "admin" and password == "admin123":
    role = "Admin"

elif username == "customer" and password == "cust123":
    role = "Customer"

elif username == "cashier" and password == "cash123":
    role = "Cashier"

else:
    role = ""

# Nested condition
if role != "":
    print(f"\nLogin successful!")
    print(f"Welcome {role}")

    # Product details
    subtotal = float(input("\nEnter subtotal amount: "))

    # Coupon code
    coupon = input("Enter coupon code: ")

    # Check coupon validity
    if coupon == "SAVE10":
        discount_percentage = 10
        print("Valid coupon code! 10% discount applied.")

    elif coupon == "SAVE20":
        discount_percentage = 20
        print("Valid coupon code! 20% discount applied.")

    else:
        discount_percentage = 0
        print("Invalid coupon code. No discount applied.")

    # Calculations
    discount_amount = subtotal * (discount_percentage / 100)

    amount_after_discount = subtotal - discount_amount

    tax_percentage = 18
    tax_amount = amount_after_discount * (tax_percentage / 100)

    final_price = amount_after_discount + tax_amount

    # Receipt
    print("\n========== RECEIPT ==========")
    print(f"User Role: {role}")
    print(f"Subtotal: UGX {subtotal:.2f}")
    print(f"Discount: UGX {discount_amount:.2f}")
    print(f"Amount after discount: UGX {amount_after_discount:.2f}")
    print(f"Tax (18%): UGX {tax_amount:.2f}")
    print(f"Final Price: UGX {final_price:.2f}")

else:
    print("Invalid username or password.")