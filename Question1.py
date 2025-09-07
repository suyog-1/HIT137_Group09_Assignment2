import random
def choose_with_vowel_bias(option1, option2):
    """
    Prefer vowels when resolving collisions:
      - If only one option is a vowel, choose it
      - If both or neither are vowels, pick randomly
    """
    vowels = "aeiouAEIOU"
    o1_is_vowel = option1 in vowels
    o2_is_vowel = option2 in vowels
    if o1_is_vowel and not o2_is_vowel:
        return option1
    elif o2_is_vowel and not o1_is_vowel:
        return option2
    else:
        # both vowel or both not vowel → random fallback
        return option1 if random.randint(1, 2) == 1 else option2
    
    
    
    
    
def encrypt_file(shift1, shift2):
    """
    Encrypt the contents of 'raw_text.txt' following the assignment rules and
    write the result to 'encrypted_text.txt'.

    Rules:
      - Lowercase a-m: shift forward by (shift1 * shift2)
      - Lowercase n-z: shift backward by (shift1 + shift2)
      - Uppercase A-M: shift backward by shift1
      - Uppercase N-Z: shift forward by (shift2 ** 2)
      - Non-alphabetic characters are unchanged

    Note: large shift values naturally wrap around via modulo 26 arithmetic.
    """
    with open('raw_text.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    encrypted = []
    for char in content:
        if 'a' <= char <= 'z':
            if char <= 'm':  # a-m
                new_char = chr((ord(char) - ord('a') + shift1 * shift2) % 26 + ord('a'))
            else:  # n-z
                new_char = chr((ord(char) - ord('a') - (shift1 + shift2)) % 26 + ord('a'))
            encrypted.append(new_char)
        elif 'A' <= char <= 'Z':
            if char <= 'M':  # A-M
                new_char = chr((ord(char) - ord('A') - shift1) % 26 + ord('A'))
            else:  # N-Z
                new_char = chr((ord(char) - ord('A') + shift2**2) % 26 + ord('A'))
            encrypted.append(new_char)
        else:
            encrypted.append(char)

    encrypted_str = ''.join(encrypted)
    with open('encrypted_text.txt', 'w', encoding='utf-8') as f:
        f.write(encrypted_str)

    print("Encrypted content:")
    print(encrypted_str)
    return encrypted_str


def decrypt_file(shift1, shift2):
    """
    Attempt to decrypt 'encrypted_text.txt' and write the reconstructed text to
    'decrypted_text.txt'.

    Because the assignment cipher can produce collisions (two different originals
    mapping to the same encrypted character), this function:
      - computes both mathematical pre-images for each alphabetic char
      - randomly picks one when both are valid (collision)
      - prints up to MAX_PRINT collision messages and then summarizes remaining
    Returns: (decrypted_string, collision_count)
    """
    with open('encrypted_text.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    decrypted = []
    collision_count = 0
    printed_messages = 0
    MAX_PRINT = 5

    for char in content:
        if 'a' <= char <= 'z':
            # inverse if original was a..m (inverse of forward shift)
            option1 = chr((ord(char) - ord('a') - shift1 * shift2) % 26 + ord('a'))
            # inverse if original was n..z (inverse of backward shift)
            option2 = chr((ord(char) - ord('a') + shift1 + shift2) % 26 + ord('a'))

            # collision: both options fall in their expected halves
            if option1 <= 'm' and option2 >= 'n':
                collision_count += 1
                chosen = option1 if random.randint(1, 2) == 1 else option2
                decrypted.append(chosen)
                if printed_messages < MAX_PRINT:
                    print(f"Collision at {char}: could be {option1} or {option2}, chose {chosen}")
                    printed_messages += 1
            elif option1 <= 'm':
                decrypted.append(option1)
            else:
                decrypted.append(option2)

        elif 'A' <= char <= 'Z':
            option1 = chr((ord(char) - ord('A') + shift1) % 26 + ord('A'))          # inverse of A..M branch
            option2 = chr((ord(char) - ord('A') - shift2**2) % 26 + ord('A'))       # inverse of N..Z branch

            if option1 <= 'M' and option2 >= 'N':
                collision_count += 1
                chosen = option1 if random.randint(1, 2) == 1 else option2
                decrypted.append(chosen)
                if printed_messages < MAX_PRINT:
                    print(f"Collision at {char}: could be {option1} or {option2}, chose {chosen}")
                    printed_messages += 1
            elif option1 <= 'M':
                decrypted.append(option1)
            else:
                decrypted.append(option2)

        else:
            decrypted.append(char)

    decrypted_str = ''.join(decrypted)
    with open('decrypted_text.txt', 'w', encoding='utf-8') as f:
        f.write(decrypted_str)

    if collision_count > printed_messages:
        remaining = collision_count - printed_messages
        print(f"...and {remaining} more collisions.")

    print(f"\nDecrypted content (had {collision_count} collisions):")
    print(decrypted_str)
    return decrypted_str, collision_count


def verify_files():
    """
    Compare 'raw_text.txt' and 'decrypted_text.txt'.
    Print the first mismatch excerpt if files differ.
    Returns True if they match exactly, False otherwise.
    """
    with open('raw_text.txt', 'r', encoding='utf-8') as f1, \
         open('decrypted_text.txt', 'r', encoding='utf-8') as f2:
        original = f1.read()
        decrypted = f2.read()

    if original == decrypted:
        print("✅ Perfect match! No errors in decryption.")
        return True

    print("❌ Decryption has errors due to collisions.")
    for i, (o_char, d_char) in enumerate(zip(original, decrypted)):
        if o_char != d_char:
            start = max(0, i - 10)
            end = min(len(original), i + 10)
            print(f"First difference at position {i}:")
            print(f"Original: ...{original[start:end]}...")
            print(f"Decrypted: ...{decrypted[start:end]}...")
            break
    return False


if __name__ == "__main__":
    try:
        shift1 = int(input("Enter shift1: "))
        shift2 = int(input("Enter shift2: "))
    except ValueError:
        print("Please enter valid integers")
        raise SystemExit(1)

    # Run the full pipeline: encrypt -> decrypt -> verify
    encrypt_file(shift1, shift2)
    decrypted, collisions = decrypt_file(shift1, shift2)
    success = verify_files()

    if collisions > 0:
        print(f"\nNote: There were {collisions} collisions during decryption.")
        print("The decryption had to make guesses, which may not always be correct.")
        print("This is a limitation of the encryption method specified in the assignment.")
