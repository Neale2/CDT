import os
import sys

PIZZA_OPTIONS = [
    ("Margherita", 10.5),
    ("Hawaiian", 10.5),
    ("Meatlovers", 10.5),
    ("Pepperoni", 10.5),
    ("BBQ Chicken", 10.5),
    ("Vegetarian", 10.5),
    ("Beef & Onion", 10.5),
    ("Lamb & Kumara", 15.5),
    ("Smoked Salmon & Cream Cheese", 15.5),
    ("Blue Cheese & Pear", 15.5),
    ("Pesto Chicken & Brie", 15.5),
    ("Mushroom & Truffle Oil", 15.5)
]

class ProgramReset(Exception):
    pass

def quit_program():
    sys.exit()

def reset_order():
    raise ProgramReset()

def custom_print(value):
    print(value)

def clear_screen():
    if 'idlelib.run' in sys.modules:
        print("\n"*49)
    else:
       os.system('cls' if os.name == 'nt' else 'clear')

       
'''
Function to add correct number of seperation dots
Start item is the item on the left of the dots, end_item is the item on the right of the dots, and desired length of combited string is desired_length.
'''

def dotter(start_item, end_item, desired_length):
    dot_quantity = desired_length - len(str(start_item)) - len(str(end_item))
    #puts correct amount of dots between string
    return "\n" + str(start_item) + "."*dot_quantity + str(end_item)


'''
Function to validate values
Value is the value to check, value_type is "Menu", "Number", "Yes/No", or "Text", size defaults to no and is max value size.
'''
def validate_value(value, value_type, size=None):
    try:
        if value == "":
            return "Must have a value!"
        #checking if response is quit or cancel
        elif value.lower() == "q" or value.lower() == "c" or value.lower() == "quit" or value.lower() == "cancel":
            return value.lower()
        #responses where only numbers are expected
        elif value_type == "Menu" or value_type == "Number":
            #will filter out any non-ints
            if not value.isdigit():
                return "Value is not a (whole) number!"
            elif int(value) < 1:
                return "Value is less than 1!"
            elif int(value) > size:
                return f"Value is higher than {size}."
            else:
                return None
        elif value_type == "Yes/No":
            if value.lower() == "y" or value.lower() == "n" or value.lower() == "no" or value.lower() == "yes":
                return None
            else:
                return "Value must be (y)es or (n)o."
        #will be value type text which needs no filtering
        else:
            return None
    except Exception as e:
        return(f"Error in program! Error message is '{e}'. Try another input.")


'''
Function to get user input
Context is the large information string displayed above, prompt is the prompt to display to users, value_type is "Menu", "Number", "Yes/No", or "Text", size defaults to no and is max value size.
'''
def get_input(context, prompt, value_type, size=None):
    #if mistake in code with wrong value type, lets me know.
    if not (value_type == "Menu" or value_type == "Text" or value_type == "Yes/No" or value_type == "Number"):
        raise ValueError("Invalid type!")
    clear_screen()
    custom_print(context)
    #validation loop
    while True:
        custom_print('[Q] Quit    [C] Cancel')
        #displays useful info depending on type
        if value_type == "Menu" or value_type == "Number":
            info_string = f"1 - {size}"
        else:
            info_string = value_type
        user_response = input(f"> {prompt}  [{info_string}]: ")

        #validates input
        validation_response = validate_value(user_response, value_type, size)

        #invalid input
        if not validation_response == None:
            if validation_response == "q" or validation_response == "quit":
                quit_program()
                #end program for now
                return None
            elif validation_response == "c" or validation_response == "cancel":
                reset_order()
                #end program for now
                return None
            else:
                clear_screen()
                custom_print(context)
                custom_print(validation_response)
        else:
            #end validation cycle
            break

    return user_response

'''
Function to generate user reciept
Order is dictionary of all the user's orders
'''
def generate_receipt(order):
    #building string to display reciept
    receipt = "      ===ORDER RECEIPT===      "
    receipt = receipt + f"\nCustomer Name: {order['name']}"
    #is order for delivery?
    if order["delivery"]:
        receipt = receipt + f"\nPhone: {order['phone']}\nAddress: {order['address']}\nDelivery"
    else:
        reciept = receipt + "\nPhone: N/A\nAddress: N/A\nNo Delivery"
    receipt = receipt + "\n-------------------------------\nItem                      Price\n"
    price = 0
    for pizza in order["pizzas"]:
        #adding nice dots to items
        receipt = receipt + dotter(pizza[0], f"${pizza[1]}", 31)
        price = price + pizza[1]
    receipt = receipt + "\n"*3 + dotter("Subtotal", f"${price}", 31)
    #is order for delivery?
    if order["delivery"]:
        price = price + 3
        receipt = receipt + "\n" + dotter("Delivery Fee", "$3.0", 31)
    else:
        receipt = receipt + "\n" + dotter("Delivery Fee", "N/A", 31)
    receipt = receipt +  "\n" * 3 + dotter("TOTAL", f"${price}", 31)
    receipt = receipt +  "\n-------------------------------\n     THANKS FOR YOUR ORDER     \n-------------------------------"

    return receipt


'''
Function to generate pizza menu
options is list of tuples, with pizza name and pizza price
'''
def generate_menu(options):
    menu = "|Pizza Topping|\n\n"
    counter = 0
    for pizza in options:
        counter = counter + 1
        menu = menu +  f"{counter}.  {pizza[0]}  - ${pizza[1]}\n"
    return (menu, counter)


'''
Function is main loop function
'''
def main():
    order = {}
    #saves lowercase first letter of response (i.e. "y" or "n")
    order["delivery"] = get_input("New Order", "Is delivery required?", "Yes/No").lower()[0]
    #formats name to be in title fomat
    order["name"] = get_input("", "Client Name", "Text").title()
    if order["delivery"] == "y":
        order["address"] = get_input("", "Client Address", "Text")
        order["phone"] = get_input("", "Client phone number", "Text")
    #save as integer
    order["quantity"] = int(get_input("", "Pizza Quantity", "Number", 5))
    menu_response = generate_menu(PIZZA_OPTIONS)
    order["pizzas"] = []
    for i in range(1, order["quantity"]):
        #put in pizza menu and length of menu
        pizza_num = int(get_input(menu_response[0], "Select topping", "Menu", menu_response[1]))
        PIZZA_OPTIONS[pizza_num].append(order["pizzas"])
    receipt = generate_receipt(order)
    get_input(receipt, "Input Q to quit or anything else to cancel/restart", "Text")
    
#main loop - if ProgramReset raised, program is reset
while True:
    try:
        main()
    except ProgramReset:
        print("Restarting order system!")



