#Program02: Python program that cleans text, computes total and distinct word counts, detects palindromes, and prints a formatted analytical report.
#Author: Manas Thakur
#Date: 12 Aug 2026

import string
from collections import Counter


def clean_text(text: str) -> list[str]:
    """Cleans punctuation, strips whitespace, and converts text to lowercased words."""
    # Remove punctuation using str.translate
    cleaned_text = text.translate(str.maketrans("", "", string.punctuation))
    # Split by whitespace into individual words
    words = cleaned_text.lower().split()
    return words


def analyze_text(text: str, min_palindrome_len: int = 3) -> dict:
    """Analyzes word frequency and identifies palindromes from plain text."""
    words = clean_text(text)

    # Word Frequency Analysis
    word_counts = Counter(words)

    # Palindrome Detection
    # Filters out single-character words by default to avoid trivial palindromes
    palindromes = sorted(
        list(
            {
                word
                for word in words
                if len(word) >= min_palindrome_len and word == word[::-1]
            }
        )
    )

    return {
        "total_words": len(words),
        "unique_words": len(word_counts),
        "word_counts": word_counts,
        "palindromes": palindromes,
    }


def generate_report(analysis: dict, top_n: int = 10) -> None:
    """Prints a formatted text analytical report."""
    print("=" * 45)
    print("      TEXT FREQUENCY & PATTERN REPORT      ")
    print("=" * 45)
    print(f"Total Word Count  : {analysis['total_words']}")
    print(f"Unique Word Count : {analysis['unique_words']}")
    print("-" * 45)

    print(f"Top {top_n} Most Frequent Words:")
    print(f"{'Word':<20} | {'Frequency':<10}")
    print("-" * 33)
    for word, count in analysis["word_counts"].most_common(top_n):
        print(f"{word:<20} | {count:<10}")

    print("-" * 45)
    print("Detected Palindromes:")
    if analysis["palindromes"]:
        print(", ".join(analysis["palindromes"]))
    else:
        print("None detected.")
    print("=" * 45)


# --- Example Usage ---
if __name__ == "__main__":
    sample_multiline_text = """
    Madam, in Eden, I'm Adam! Was it a car or a cat I saw?
    The level of detail in this radar system is top-notch.
    Word counts help us analyze text patterns. Text patterns tell a story.
    Madam, check the level again!
    """

    # Run analysis
    results = analyze_text(sample_multiline_text)

    # Display report
    generate_report(results)
