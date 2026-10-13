class PhonebookManager:
    def __init__(self):
        # In-memory dictionary to store structured contact entries
        self.directory = {}

    def add_contact(self, contact_id, name, phone, email):
        """Stores a new structured contact record dynamically."""
        self.directory[contact_id] = {
            "name": name,
            "phone": phone,
            "email": email
        }
        print(f"Contact '{name}' added successfully.")

    def remove_contact(self, contact_id):
        """Removes a contact record dynamically."""
        if contact_id in self.directory:
            removed = self.directory.pop(contact_id)
            print(f"Removed contact: {removed['name']}")
        else:
            print("Contact ID not found.")

    def update_fields_bulk(self, field_name, old_value, new_value):
        """
        Updates a specific field for all contacts matching an old value.
        Demonstrates the use of .values() and list comprehensions for field updates.
        """
        # List comprehension to find contacts that need updating
        contacts_to_update = [
            contact for contact in self.directory.values() 
            if contact.get(field_name) == old_value
        ]
        
        for contact in contacts_to_update:
            contact[field_name] = new_value
        print(f"Updated {len(contacts_to_update)} records.")

    def dynamic_lookup(self, search_term):
        """
        Queries the directory for a search term across all fields.
        Demonstrates the use of .items() and list comprehensions for dynamic lookup.
        """
        # List comprehension using .items() and .values() to find matches
        matches = [
            (c_id, details) for c_id, details in self.directory.items()
            if search_term.lower() in str(details.values()).lower()
        ]
        return matches

    def display_all_keys(self):
        """Demonstrates the use of the .keys() view method."""
        print("Current Contact IDs in Directory:")
        # Using .keys() to retrieve all primary keys
        for c_id in self.directory.keys():
            print(f"- {c_id}")

# --- Example Usage ---
if __name__ == "__main__":
    pb = PhonebookManager()
    
    # Store records
    pb.add_contact("C001", "Alice Smith", "555-0101", "alice@example.com")
    pb.add_contact("C002", "Bob Jones", "555-0102", "bob@old-domain.com")
    pb.add_contact("C003", "Charlie Brown", "555-0103", "charlie@old-domain.com")
    
    # Use .keys() view
    pb.display_all_keys()
    
    # Dynamic field update (Update domain for multiple contacts)
    pb.update_fields_bulk("email", "bob@old-domain.com", "bob@new-domain.com")
    
    # Dynamic lookup query using list comprehensions and .items()
    print("\nSearch Results for '555':")
    results = pb.dynamic_lookup("555")
    for r in results:
        print(r)
        
    # Remove a contact
    pb.remove_contact("C001")