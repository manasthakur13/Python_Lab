def clean_text(text):
    """Cleans formatting variances (e.g., spaces, capitalization) for accurate matching."""
    return "".join(text.lower().split())

def is_anagram_sorting(text1, text2):
    """
    Determines if two phrases are anagrams using list sorting algorithms.
    """
    # Sorting the cleaned character arrays to check for equivalence
    return sorted(list(clean_text(text1))) == sorted(list(clean_text(text2)))

def is_anagram_counting(text1, text2):
    """
    Determines if two phrases are anagrams using dictionary counting techniques.
    """
    cleaned1, cleaned2 = clean_text(text1), clean_text(text2)
    if len(cleaned1) != len(cleaned2):
        return False
        
    char_count = {}
    
    # Populate the frequency dictionary for the first phrase
    for char in cleaned1:
        char_count[char] = char_count.get(char, 0) + 1
        
    # Decrement the counts based on the second phrase
    for char in cleaned2:
        if char not in char_count or char_count[char] == 0:
            return False
        char_count[char] -= 1
        
    return True

def group_anagrams_fast_lookup(phrase_list):
    """
    Groups anagrams together using immutable tuple keys to perform fast lookup matchings.
    """
    anagram_groups = {}
    for phrase in phrase_list:
        # A sorted tuple of characters acts as a secure, immutable tuple key for the dictionary
        key = tuple(sorted(clean_text(phrase)))
        
        if key not in anagram_groups:
            anagram_groups[key] = []
        anagram_groups[key].append(phrase)
        
    return list(anagram_groups.values())

# --- Example Usage ---
if __name__ == "__main__":
    word1 = "Listen"
    word2 = "Silent "
    
    print(f"Using Sorting: '{word1}' & '{word2}' -> {is_anagram_sorting(word1, word2)}")
    print(f"Using Counting: '{word1}' & '{word2}' -> {is_anagram_counting(word1, word2)}")
    
    phrases = ["Dormitory", "Dirty room", "Astronomer", "Moon starer", "Hello", "World"]
    print("\nGrouped Anagram Patterns:")
    grouped = group_anagrams_fast_lookup(phrases)
    for group in grouped:
        if len(group) > 1:
            print(f"Match Found: {group}")