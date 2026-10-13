class InventoryTracker:
    def __init__(self):
        # Representing individual store location dictionaries
        self.store_a_stock = {"laptops": 15, "monitors": 30, "cables": 100}
        self.store_b_stock = {"monitors": 20, "keyboards": 45, "mice": 60}

    def check_item_stock(self, store, item_name):
        """Safely accesses fields via .get() to avoid KeyErrors."""
        stock_level = store.get(item_name, 0)
        print(f"Stock for '{item_name}': {stock_level}")
        return stock_level

    def restock_item(self, store, item_name, quantity):
        """Makes use of key existence checks to update or add inventory."""
        if item_name in store:
            store[item_name] += quantity
            print(f"Updated existing item '{item_name}'. New total: {store[item_name]}")
        else:
            store[item_name] = quantity
            print(f"Added new item '{item_name}' with quantity: {quantity}")

    def merge_inventories_comprehension(self):
        """
        Merges multiple stock records to find total company inventory 
        using dictionary comprehension patterns.
        """
        all_items = set(self.store_a_stock.keys()).union(set(self.store_b_stock.keys()))
        
        # Dictionary comprehension to sum quantities across both store locations
        total_inventory = {
            item: self.store_a_stock.get(item, 0) + self.store_b_stock.get(item, 0)
            for item in all_items
        }
        return total_inventory

    def merge_inventories_update_operator(self):
        """
        Merges dictionaries using the Python 3.9+ update operator (|).
        This overwrites overlapping keys with values from the right-side dictionary.
        """
        # Merging multiple stock records utilizing the union/update operator
        merged_stock = self.store_a_stock | self.store_b_stock
        return merged_stock

# --- Example Usage ---
if __name__ == "__main__":
    tracker = InventoryTracker()
    
    print("--- Safe Access (.get) ---")
    tracker.check_item_stock(tracker.store_a_stock, "monitors")
    tracker.check_item_stock(tracker.store_a_stock, "webcams") # Doesn't exist, safely returns 0
    
    print("\n--- Key Existence Checks ---")
    tracker.restock_item(tracker.store_a_stock, "laptops", 5) # Existing
    tracker.restock_item(tracker.store_a_stock, "webcams", 20) # New
    
    print("\n--- Dictionary Comprehension Merging (Sum) ---")
    total_stock = tracker.merge_inventories_comprehension()
    for item, qty in total_stock.items():
        print(f"{item}: {qty}")
        
    print("\n--- Update Operator Merging (Overwrite from Store B) ---")
    overwrite_stock = tracker.merge_inventories_update_operator()
    for item, qty in overwrite_stock.items():
        print(f"{item}: {qty}")