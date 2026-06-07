import json

try:
    with open("contacts.json", "r") as file:
        contacts = json.load(file)
except FileNotFoundError:


    contacts = {}
print("Welcome to the Contact Management System")
while True:
    print("\nOptions: add, delete, search, update,  display, quit")
    choice = input("What would you like to do:")
    if choice == "add":
        name = input ("Enter the name of the contact:")
        phone = input ("Enter the contact number:")
        contacts[name] = phone
        print("Contact has been successfully added")
    elif choice == "delete":
        name = input ("Enter the name of the contact you would like to delete:")
        if name in contacts:
            del contacts[name]
            print("Contract Successfully deleted")
        else:
            print("Contact not found")    
    elif choice == "search":
        search = input ("Enter the name of the contact you would like to view: ")
        if search in contacts:
            print("The contact you searched for is:\n", search, "-", contacts[search])
        else:
            print("Contact not found")
    elif choice == "update":
        name = input ("Enter the name of the contact you would like to update: ")
        if name in contacts:
            new_phone = input ("Enter new phone number: ")
            contacts[name] = new_phone
            print ("Contact successfully updated")
        else:
            print("Contact not found")
    elif choice == "display":
        print("\nSaved Contacts");
        for name, phone in contacts.items():
            print(name, "-" ,phone)
    elif choice == "quit":
        with open("contacts.json", "w") as file:
            json.dump(contacts, file)
        print("Contacts saved to contacts.json.")
        break