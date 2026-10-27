import pickle
import shelve
import os

class UserProfile:
    """
    A complex class instance representing a user's profile and settings.
    This object's live state will be persisted to disk.
    """
    def __init__(self, username, level, preferences):
        self.username = username
        self.level = level
        self.preferences = preferences

    def update_level(self, new_level):
        """Updates the user's level."""
        self.level = new_level

    def __str__(self):
        """Returns a string representation of the user profile."""
        return f"User: {self.username} | Level: {self.level} | Prefs: {self.preferences}"


def persist_with_pickle(obj, filename):
    """
    Converts a complex class instance into a binary stream and writes it 
    safely to disk using the built-in pickle module.
    
    Args:
        obj (object): The Python object to serialize.
        filename (str): The destination file path.
    """
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)
    print(f"Object successfully persisted to {filename} via pickle.")


def restore_with_pickle(filename):
    """
    Reads and restores object states back into memory from a binary file.
    
    Args:
        filename (str): The source file path.
        
    Returns:
        object: The restored Python object.
    """
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            obj = pickle.load(file)
        print(f"Object successfully restored from {filename} via pickle.")
        return obj
    else:
        print(f"Error: {filename} not found.")
        return None


def manage_with_shelve(db_name, key, obj=None, action="save"):
    """
    Persists or retrieves live Python object states to disk across 
    execution runs using the built-in shelve module.
    
    Args:
        db_name (str): The shelve database filename.
        key (str): The dictionary key under which the object is stored.
        obj (object, optional): The object to store (if action is "save").
        action (str): Either "save" or "load".
        
    Returns:
        object or None: The restored object if action is "load".
    """
    with shelve.open(db_name) as db:
        if action == "save":
            db[key] = obj
            print(f"Object saved to shelve database '{db_name}' under key '{key}'.")
        elif action == "load":
            obj = db.get(key)
            if obj:
                print(f"Object restored from shelve database '{db_name}' under key '{key}'.")
                return obj
            else:
                print(f"Key '{key}' not found in shelve database '{db_name}'.")
                return None


def main():
    """Main execution function to demonstrate object persistence."""
    # 1. Create a complex class instance
    user = UserProfile("CyberNinja99", 42, {"theme": "dark", "notifications": True})
    print("Original Object State:")
    print(user)
    
    # 2. Persist using Pickle
    pickle_file = "user_data.pkl"
    persist_with_pickle(user, pickle_file)
    
    # Modify the original object to prove we load the old state
    user.update_level(100)
    print("\nModified In-Memory Object State (Not Saved):")
    print(user)
    
    # Restore using Pickle
    restored_user_pickle = restore_with_pickle(pickle_file)
    print("\nRestored Object State (Pickle):")
    print(restored_user_pickle)
    
    print("-" * 40)
    
    # 3. Persist using Shelve
    shelve_db = "app_data_shelve"
    shelve_key = "user_1"
    
    manage_with_shelve(shelve_db, shelve_key, obj=user, action="save")
    
    # Restore using Shelve
    restored_user_shelve = manage_with_shelve(shelve_db, shelve_key, action="load")
    print("\nRestored Object State (Shelve):")
    print(restored_user_shelve)

if __name__ == "__main__":
    main()