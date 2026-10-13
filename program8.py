def calculate_grade_statistics(*args, **kwargs):
    """
    Computes class performance scores from variable assessment grades.
    *args captures an arbitrary number of numerical grades.
    **kwargs captures dynamic metadata like student name, course name, or semester.
    """
    if not args:
        return None, None, None, {}, kwargs

    # Calculate min, max, and average from the variable-length *args tuple
    min_grade = min(args)
    max_grade = max(args)
    avg_grade = sum(args) / len(args)

    # Calculate letter score distributions using a dictionary
    letter_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for grade in args:
        if grade >= 90:
            letter_distribution['A'] += 1
        elif grade >= 80:
            letter_distribution['B'] += 1
        elif grade >= 70:
            letter_distribution['C'] += 1
        elif grade >= 60:
            letter_distribution['D'] += 1
        else:
            letter_distribution['F'] += 1

    # Returns multiple structured metrics
    return min_grade, max_grade, avg_grade, letter_distribution, kwargs

# --- Example Usage & Tuple Unpacking ---
if __name__ == "__main__":
    # Passing varying sets of assessment grades (*args) and metadata (**kwargs)
    result = calculate_grade_statistics(85, 92, 78, 99, 65, 88, 73, 
                                        student="John Doe", 
                                        course="Computer Science 101", 
                                        term="Fall 2026")

    # Returning multiple structured metrics via tuple unpacking
    minimum, maximum, average, distribution, metadata = result

    print(f"Student Data: {metadata}")
    print(f"Lowest Grade: {minimum}")
    print(f"Highest Grade: {maximum}")
    print(f"Average Grade: {average:.2f}")
    print(f"Letter Distribution: {distribution}")