import secrets
import string

def generate_password(length, numbers=True, special_characters=True):
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation

    characters = letters

    if numbers:
        characters += digits

    if special_characters:
        characters += special

    while True:
        password = ""

        for _ in range(length):
            password += secrets.choice(characters)

        has_number = any(char in digits for char in password)
        has_special = any(char in special for char in password)

        if numbers and not has_number:
            continue

        if special_characters and not has_special:
            continue

        return password


print(generate_password(12))