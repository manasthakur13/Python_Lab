import sys


def caesar_cipher(text, displacement, mode):
  """Encrypts or decrypts the given text using a Caesar cipher.

  - mode: 'e' for encrypt, 'd' for decrypt
  """
  result = []

  # If decrypting, reverse the displacement
  if mode == "d":
    displacement = -displacement

  for char in text:
    # Check if the character is an alphabet letter using string methods
    if char.isalpha():
      # Determine the ASCII offset for uppercase ('A') or lowercase ('a')
      ascii_offset = ord("A") if char.isupper() else ord("a")

      # Apply the shift formula and wrap around the alphabet using modulo 26
      shifted_char = chr(
          (ord(char) - ascii_offset + displacement) % 26 + ascii_offset
      )
      result.append(shifted_char)
    else:
      # Leave non-alphabetic characters (spaces, punctuation) unchanged
      result.append(char)

  return "".join(result)


def main():
  # Validate command line arguments count
  # Expected: python cipher.py <flag> <text> <displacement>
  if len(sys.argv) != 4:
    print(
        "Usage: python cipher.py <-e|-d> <text> <displacement>",
        file=sys.stderr,
    )
    print("Example: python cipher.py -e 'Hello, World!' 3", file=sys.stderr)
    sys.exit(1)

  flag = sys.argv[1]
  text = sys.argv[2]

  try:
    displacement = int(sys.argv[3])
  except ValueError:
    print("Error: Displacement must be an integer.", file=sys.stderr)
    sys.exit(1)

  # Validate the flag
  if flag == "-e":
    mode = "e"
  elif flag == "-d":
    mode = "d"
  else:
    print(
        f"Error: Invalid flag '{flag}'. Use '-e' to encrypt or '-d' to decrypt.",
        file=sys.stderr,
    )
    sys.exit(1)

  # Process and print the result
  output_text = caesar_cipher(text, displacement, mode)
  print(output_text)


if __name__ == "__main__":
  main()