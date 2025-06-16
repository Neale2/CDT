import os
import sys

def quit_program():
    print("force program to quit")

def reset_order():
    print("reset order")

def custom_print(value):
    print(value)

def clear_screen():
    if 'idlelib.run' in sys.modules:
        print("\n"*49)
    else:
       os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

'''
Value is the value to check, value_type is "Menu", "Number", "Yes/No", or "Text", size defaults to no and is max value size.
'''
def validate_value(value, value_type, size=None):
    try:
        if value == "":
            return "Must have a value!"
        #checking if response is quit or cancel
        elif value.lower() == "q" or value.lower() == "c":
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
            if validation_response == "q":
                quit_program()
                #end program for now
                return None
            elif validation_response == "c":
                reset_order()
                #end program for noe
                return None
            else:
                clear_screen()
                custom_print(context)
                custom_print(validation_response)
        else:
            #end validation cycle
            break

    return user_response

                    
    
