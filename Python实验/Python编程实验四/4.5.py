def search_contact(name, filename='contacts.txt'):
    with open(filename, 'r') as file:
        for line in file:
            contact_name, phone_number = line.strip().split(',')
            if name == contact_name:
                return f"Name: {contact_name}, Phone Number: {phone_number}"

    return "Not Found"

input_name = input("Enter the name to search: ")
result = search_contact(input_name)

print(result)
