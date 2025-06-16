'''
Value is the value to check, value_type is "Menu", "Number", "Yes/No", or "Text", size defaults to no and is max value size.
'''

def validate_value(value, value_type, size=None):
    #wrap in try/except
    
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
        elif value > size:
            return f"Value is higher than {size}"
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
        
