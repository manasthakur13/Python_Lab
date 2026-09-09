import os
import sys


def parse_arguments():
    # Extracts target directory and file extension filter from CLI arguments
    target_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    ext_filter = sys.argv[2] if len(sys.argv) > 2 else None
    return os.path.abspath(target_dir), ext_filter


def list_directory(target_dir, ext_filter=None):
    if not os.path.exists(target_dir):
        print(f"Error: Directory '{target_dir}' does not exist.")
        return

    print(f"\nScanning: {target_dir}")
    try:
        entries = os.listdir(target_dir)
        for item in entries:
            full_path = os.path.join(target_dir, item)
            if os.path.isdir(full_path):
                print(f"  [DIR]  {item}")
            else:
                # Filter by extension if argument was provided
                if ext_filter is None or item.endswith(ext_filter):
                    size = os.path.getsize(full_path)
                    print(f"  [FILE] {item:<25} ({size} bytes)")
    except PermissionError:
        print(f"Error: Access denied for '{target_dir}'.")


def create_workspace(base_dir, folder_name):
    workspace_path = os.path.join(base_dir, folder_name)
    # Safely creates directory without throwing an error if it exists
    os.makedirs(workspace_path, exist_ok=True)
    print(f"Workspace initialized: {workspace_path}")
    return workspace_path


def write_log(workspace_path, log_name, content):
    log_path = os.path.join(workspace_path, log_name)
    # Context manager automatically closes file descriptor upon exit/error
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(content + "\n")
    print(f"Appended entry to log: {log_path}")


def read_log(workspace_path, log_name):
    log_path = os.path.join(workspace_path, log_name)
    if not os.path.exists(log_path):
        print(f"Log file not found: {log_path}")
        return

    # Context manager ensures safe-read without resource leaks
    with open(log_path, "r", encoding="utf-8") as f:
        print(f"\n--- Log Contents: {log_name} ---")
        for line in f:
            print(f" > {line.strip()}")


def main():
    current_dir, extension = parse_arguments()

    while True:
        print("\n=== File & Directory Management Utility ===")
        print(f"Active Directory: {current_dir}")
        print("1. List Directory Contents")
        print("2. Navigate to Subdirectory / Change Path")
        print("3. Create Dynamic Workspace Folder")
        print("4. Append Entry to Log File")
        print("5. Read Target Log File")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            list_directory(current_dir, extension)

        elif choice == "2":
            sub_path = input("Enter directory name or full path: ").strip()
            # Resolve relative or absolute path based on input
            resolved_path = (
                sub_path
                if os.path.isabs(sub_path)
                else os.path.join(current_dir, sub_path)
            )
            resolved_path = os.path.abspath(resolved_path)

            if os.path.isdir(resolved_path):
                current_dir = resolved_path
                os.chdir(current_dir)
                print(f"Working directory updated to: {current_dir}")
            else:
                print("Invalid directory path.")

        elif choice == "3":
            folder_name = input("Enter workspace folder name: ").strip()
            if folder_name:
                create_workspace(current_dir, folder_name)
            else:
                print("Folder name cannot be empty.")

        elif choice == "4":
            log_name = input("Enter log file name (e.g., audit.log): ").strip()
            text_data = input("Enter text content to append: ").strip()
            if log_name:
                write_log(current_dir, log_name, text_data)
            else:
                print("File name cannot be empty.")

        elif choice == "5":
            log_name = input("Enter log file name to read: ").strip()
            if log_name:
                read_log(current_dir, log_name)
            else:
                print("File name cannot be empty.")

        elif choice == "6":
            print("Terminating utility.")
            sys.exit(0)

        else:
            print("Invalid option. Enter a number between 1 and 6.")


if __name__ == "__main__":
    main()