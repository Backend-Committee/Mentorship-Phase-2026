print("Hello welcome to our store!")
print()

# Mission 1
# Create a dictionary to store some products (4 or 5) the name and the price
store_items = {}

# Mission 2
# Create an empty list to store the products the customer picked * name it cart

# Mission 3
# Create a decorator func to apply a 10% discount if the total price is over 60 pound
def discount(func):
    def wrapper():
        total = func()
        # write the rest here
        return total
    return wrapper

# Mission 4
# do the func that calculate the total price
                # call the decorator you did here
def calc_total():
    total = 0
    # loop on cart and calculate the total
    return total

# Mission 5
# The Menu
print("The products we have are")
# loop on the dictionary to view every product on an independent line and the price next to it
print("to checkout write exit")
while True:
    #user_input = # take the input from the user ask him for the name of the product

    if user_input == "exit":
        break

    # Create a condition to check if user_input is a product (key in dictionary) and if yes add it to the cart(list)

    else:
        print("there is no such product")


# Mission 6
# the output
print("###############The Bill###############")
# you should use the formatted string literal (f"{}") to handel printing useful messages
# print the products the user picked
# print the total price using the func you did use






