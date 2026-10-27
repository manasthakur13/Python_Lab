import traceback
import os

# --- Custom Exception Hierarchy ---
class FileProcessingError(Exception):
    """
    Base class for custom exceptions in the file processing pipeline.
    """
    pass


class InvalidFormatError(FileProcessingError):
    """
    Application-specific exception class to flag invalid file formatting.
    Raised when the file content does not match the expected structural rules.
    """
    def __init__(self, message="Invalid file format detected during parsing."):
        self.message = message
        super().__init__(self.message)


# --- File Processing Pipeline ---
def parse_file_pipeline(filepath):
    """
    A fault-tolerant file parsing pipeline that attempts to read and process
    comma-separated integer data from a text file.
    
    Args:
        filepath (str): The path to the file to be processed.
    
    Returns:
        list: A list of parsed integers if successful, or None if an error occurred.
    """
    file_resource = None
    
    try:
        print(f"Attempting to open and parse: '{filepath}'")
        # Opening file manually to demonstrate explicit resource cleanup in the 'finally' block
        file_resource = open(filepath, 'r')
        data = file_resource.read().strip()
        
        if not data:
            raise ValueError("The file is empty.")
            
        parsed_numbers = []
        # Simulate parsing a specific format: expecting only comma-separated numbers
        for item in data.split(','):
            item = item.strip()
            if not item.isdigit():
                # Raise our custom exception if the data is not a valid integer
                raise InvalidFormatError(f"Format violation: '{item}' is not a valid integer.")
            parsed_numbers.append(int(item))
            
    except FileNotFoundError as e:
        print(f"Runtime Error: The file '{filepath}' could not be located.")
        print("Traceback Log:")
        print(traceback.format_exc())
        
    except InvalidFormatError as e:
        print(f"Custom Application Error: {e}")
        print("Traceback Log:")
        print(traceback.format_exc())
        
    except Exception as e:
        # Catches any other unforeseen runtime errors
        print(f"Unexpected Runtime Error: {e}")
        print("Traceback Log:")
        print(traceback.format_exc())
        
    else:
        # Executes ONLY if the try block completes without any exceptions
        print("Success: File successfully parsed without any errors.")
        print(f"Extracted Data: {parsed_numbers}")
        return parsed_numbers
        
    finally:
        # This block executes no matter what, guaranteeing safe resource cleanup
        if file_resource is not None and not file_resource.closed:
            file_resource.close()
            print("Cleanup: File resource safely closed via 'finally' block.")
        print("--- Execution pipeline finished ---\n")
        

def main():
    """
    Main execution function to demonstrate the fault-tolerant exception handling.
    """
    # 1. Test with a non-existent file (Triggers FileNotFoundError)
    parse_file_pipeline("missing_data_file.txt")
    
    # Setup temporary test files
    valid_file = "valid_data.txt"
    invalid_file = "invalid_data.txt"
    
    with open(valid_file, 'w') as f:
        f.write("100, 200, 300, 400")
        
    with open(invalid_file, 'w') as f:
        f.write("100, 200, error_string, 400")
        
    # 2. Test with a valid file (Triggers 'else' block)
    parse_file_pipeline(valid_file)
    
    # 3. Test with a badly formatted file (Triggers custom InvalidFormatError)
    parse_file_pipeline(invalid_file)
    
    # Clean up the temporary files from the disk
    if os.path.exists(valid_file):
        os.remove(valid_file)
    if os.path.exists(invalid_file):
        os.remove(invalid_file)

if __name__ == "__main__":
    main()