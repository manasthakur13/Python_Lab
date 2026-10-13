def clean_matrix_noise(matrix):
    """
    Filters out negative matrix noise from a 2D list/tuple structure.
    Uses map(), filter(), and lambda expressions to process nested lists.
    """
    # map() applies the lambda to each row in the 2D matrix
    # filter() uses a lambda to keep only non-negative elements (x >= 0)
    # The result is cast back to a tuple to maintain sequence structure
    cleaned = tuple(
        map(lambda row: tuple(filter(lambda x: x >= 0, row)), matrix)
    )
    return cleaned

def sort_matrix_by_custom_key(matrix, descending=True):
    """
    Sorts matrix entries (rows) using a custom key.
    Uses sorted() and a lambda expression as the sorting key.
    """
    # sorted() orders the rows. 
    # lambda row: sum(row) calculates the sum of the row to use as the sorting key.
    sorted_matrix = sorted(matrix, key=lambda row: sum(row), reverse=descending)
    return sorted_matrix

def transform_and_scale(matrix, scale_factor):
    """
    Applies a mathematical transformation (scaling) to the matrix.
    Uses map() and lambda to multiply every element by the scale factor.
    """
    # Nested map() calls with lambdas to multiply each item 'x' by the scale factor
    transformed = tuple(
        map(lambda row: tuple(map(lambda x: x * scale_factor, row)), matrix)
    )
    return transformed

# --- Example Usage ---
if __name__ == "__main__":
    # Initial 2D computational data sequence with negative "noise"
    raw_matrix = (
        (10, -5, 3, 8),
        (-2, 15, -1, 4),
        (0, 7, 2, -9),
        (12, 1, 5, 2)
    )
    
    print("Original Raw Matrix:")
    for row in raw_matrix: print(row)

    # 1. Filter out negative matrix noise
    cleaned_matrix = clean_matrix_noise(raw_matrix)
    print("\nAfter Filtering Negative Noise (map, filter, lambda):")
    for row in cleaned_matrix: print(row)

    # 2. Sort entries using custom keys (sorting by the sum of the row)
    sorted_matrix = sort_matrix_by_custom_key(cleaned_matrix, descending=True)
    print("\nAfter Sorting by Row Sum (sorted, lambda):")
    for row in sorted_matrix: print(f"{row} (Sum: {sum(row)})")

    # 3. Transform the computational data sequence (scale by 10)
    final_matrix = transform_and_scale(sorted_matrix, scale_factor=10)
    print("\nAfter Scaling Transformation (nested map, lambda):")
    for row in final_matrix: print(row)