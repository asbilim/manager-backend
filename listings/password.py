import random
import string
import os

def generate_password(path = os.path.join(os.path.dirname(__file__), 'word.txt')):
    
    with open(path, 'r') as f:
        words = f.read().splitlines()
    
    # Randomly select a word from the list
    word = random.choice(words)

    # Character replacements
    replacements = {
        'a': '4',
        'e': '3',
        'i': '1',
        'o': '0',
        's': '5',
        't': '7',
    }

    # Replace characters and capitalize the first letter
    password = "".join(replacements.get(c, c) for c in word)
    password = password[0].upper() + password[1:]

    # Add random numbers and special characters
    num_digits = random.randint(2, 4)
    digits = ''.join(random.choices(string.digits, k=num_digits))
    symbols = ''.join(random.choices(string.punctuation, k=num_digits))

    password += f'_{digits}{symbols}'

    return password
