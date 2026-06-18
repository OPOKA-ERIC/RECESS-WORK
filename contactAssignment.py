class ContactManager:
    def __init__(self):
        self.contacts = []

    def validate_phone(self, phone):
        allowed = set("0123456789-+")
        for ch in phone:
            if ch not in allowed:
                print(f"Error: Phone number contains invalid character '{ch}'. Only digits, hyphens, and + allowed.")
                return False
        return True

    def validate_email(self, email):
        if email == "":
            return True
        if "@" not in email or "." not in email:
            print("Error: Email must contain '@' and '.' symbols.")
            return False
        at_index = email.index("@")
        dot_index = email.rindex(".")
        if at_index == 0 or dot_index <= at_index + 1 or dot_index == len(email) - 1:
            print("Error: Email format is invalid.")
            return False
        return True

    def add_contact(self, name, phone, email=""):
        if not self.validate_phone(phone):
            return
        if not self.validate_email(email):
            return
        self.contacts.append([name, phone, email])
        print(f"Contact '{name}' added successfully!")

    def view_contact(self, name):
        for c in self.contacts:
            if c[0].lower() == name.lower():
                print(f"Name: {c[0]}")
                print(f"Phone: {c[1]}")
                print(f"Email: {c[2]}")
                return
        print(f"Contact '{name}' not found.")

    def update_contact(self, name, phone=None, email=None):
        for c in self.contacts:
            if c[0].lower() == name.lower():
                if phone is not None:
                    if not self.validate_phone(phone):
                        return
                    c[1] = phone
                if email is not None:
                    if not self.validate_email(email):
                        return
                    c[2] = email
                print(f"Contact '{name}' updated successfully!")
                return
        print(f"Contact '{name}' not found.")

    def delete_contact(self, name):
        for c in self.contacts:
            if c[0].lower() == name.lower():
                self.contacts.remove(c)
                print(f"Contact '{name}' deleted successfully!")
                return
        print(f"Contact '{name}' not found.")

    def search_contacts(self, query):
        results = []
        query_lower = query.lower()
        for c in self.contacts:
            if query_lower in c[0].lower() or query_lower in c[1] or query_lower in c[2].lower():
                results.append(c)
        if results:
            print(f"\nFound {len(results)} contact(s):")
            print("-" * 50)
            print(f"{'Name':20s} {'Phone':20s} {'Email':25s}")
            print("-" * 50)
            for c in results:
                print(f"{c[0]:20s} {c[1]:20s} {c[2]:25s}")
            print("-" * 50)
        else:
            print("No contacts found matching your search.")
        return results

    def list_all_contacts(self):
        if not self.contacts:
            print("No contacts in the list.")
            return
        print(f"\nTotal Contacts: {len(self.contacts)}")
        print("=" * 60)
        print(f"{'#':3s} {'Name':20s} {'Phone':20s} {'Email':25s}")
        print("=" * 60)
        for i, c in enumerate(self.contacts, 1):
            print(f"{i:3d} {c[0]:20s} {c[1]:20s} {c[2]:25s}")
        print("=" * 60)


def main():
    manager = ContactManager()

    while True:
        print()
        print("=== Contact Manager Menu ===")
        print("1. Add Contact")
        print("2. View Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Search Contacts")
        print("6. List All Contacts")
        print("7. Exit")
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            name = input("Enter name: ").strip()
            phone = input("Enter phone: ").strip()
            email = input("Enter email (optional): ").strip()
            manager.add_contact(name, phone, email)

        elif choice == "2":
            name = input("Enter name to view: ").strip()
            manager.view_contact(name)

        elif choice == "3":
            name = input("Enter name to update: ").strip()
            phone = input("Enter new phone (leave blank to keep): ").strip()
            email = input("Enter new email (leave blank to keep): ").strip()
            manager.update_contact(name, phone if phone else None, email if email else None)

        elif choice == "4":
            name = input("Enter name to delete: ").strip()
            manager.delete_contact(name)

        elif choice == "5":
            query = input("Enter search term: ").strip()
            manager.search_contacts(query)

        elif choice == "6":
            manager.list_all_contacts()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-7.")


if __name__ == "__main__":
    main()
